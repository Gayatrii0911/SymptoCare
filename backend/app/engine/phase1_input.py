"""
Phase 1: User Context & Input Understanding
============================================
Parses raw user input, normalizes symptoms via NLP, detects language.
Uses the NLP engine for:
  • phrase-based extraction (500+ natural-language aliases)
  • negation detection  ("I don't have fever")
  • clause-level independence
  • direct column-name matching
"""

from app.models import UserProfile, TriageInput
from app.engine.knowledge_base import (
    SYMPTOM_SYNONYMS,
    HINDI_MARKERS,
    MARATHI_MARKERS,
)
from app.engine.nlp import extract_symptoms_nlp, NLP_PHRASE_MAP
from ml.predictor import get_all_symptoms


def detect_language(text: str) -> str:
    """Detect input language from text using keyword markers."""
    text_lower = text.lower()
    hindi_score = sum(1 for w in HINDI_MARKERS if w in text_lower)
    marathi_score = sum(1 for w in MARATHI_MARKERS if w in text_lower)

    if marathi_score >= 2:
        return "mr"
    if hindi_score >= 2:
        return "hi"
    return "en"


def normalize_symptoms_from_text(raw_text: str) -> tuple[list[str], list[str]]:
    """
    Extract and normalize symptoms from free-text using the NLP engine.
    Returns:
        (normalized_symptoms, negated_symptoms)
    """
    return extract_symptoms_nlp(raw_text)


def normalize_symptom_list(symptom_list: list[str]) -> list[str]:
    """
    Normalize a pre-selected list of symptoms (chip/dropdown selection).
    Ensures names match the ML model's expected columns.
    """
    all_symptoms = set(get_all_symptoms())
    normalized = set()

    for symptom in symptom_list:
        s = symptom.strip().lower()
        # Direct match
        if s in all_symptoms:
            normalized.add(s)
            continue
        # Try with underscore replacement
        s_under = s.replace(" ", "_")
        if s_under in all_symptoms:
            normalized.add(s_under)
            continue
        # Check NLP phrase map first (more comprehensive)
        if s in NLP_PHRASE_MAP:
            normalized.add(NLP_PHRASE_MAP[s])
            continue
        # Fallback to legacy synonym map
        if s in SYMPTOM_SYNONYMS:
            mapped = SYMPTOM_SYNONYMS[s]
            if mapped in all_symptoms:
                normalized.add(mapped)

    return sorted(normalized)


def process_input(data: dict) -> TriageInput:
    """
    Phase 1 main entry point.

    Accepts:
        {
            "age": int,
            "gender": str,
            "symptoms": list[str] | str,
            "raw_text": str (optional free-text),
            "input_method": "text" | "voice",
            "language": "en" | "hi" | "mr" (optional)
        }

    Returns: TriageInput object
    """
    age = data.get("age")
    gender = data.get("gender", "").strip().lower()
    input_method = data.get("input_method", "text")
    raw_text = data.get("raw_text", "")
    symptoms_input = data.get("symptoms", [])

    negated: list[str] = []

    # ── NLP-based extraction ──────────────────────────────────────────
    if isinstance(symptoms_input, list) and symptoms_input:
        # Chip-selected symptoms: normalize directly
        normalized = normalize_symptom_list(symptoms_input)
    elif raw_text:
        normalized, negated = normalize_symptoms_from_text(raw_text)
    elif isinstance(symptoms_input, str) and symptoms_input:
        normalized, negated = normalize_symptoms_from_text(symptoms_input)
    else:
        normalized = []

    # Also run NLP on raw_text for additional symptoms
    if raw_text and isinstance(symptoms_input, list) and symptoms_input:
        text_symptoms, text_negated = normalize_symptoms_from_text(raw_text)
        for s in text_symptoms:
            if s not in normalized:
                normalized.append(s)
        negated.extend(text_negated)
        normalized.sort()

    # ── Language detection ────────────────────────────────────────────
    language = data.get("language", "")
    if not language and raw_text:
        language = detect_language(raw_text)
    if not language and isinstance(symptoms_input, str) and symptoms_input:
        language = detect_language(symptoms_input)
    if not language:
        language = "en"

    # ── Build raw symptoms string for downstream phases ───────────────
    if raw_text:
        raw_symptoms = raw_text
    elif isinstance(symptoms_input, list):
        raw_symptoms = ", ".join(symptoms_input)
    else:
        raw_symptoms = str(symptoms_input)

    triage_input = TriageInput(
        raw_symptoms=raw_symptoms,
        normalized_symptoms=normalized,
        user_profile=UserProfile(age=age, gender=gender),
        input_language=language,
        input_method=input_method,
    )

    # Attach NLP metadata for pipeline to surface in response
    triage_input._negated_symptoms = negated  # type: ignore[attr-defined]

    return triage_input
