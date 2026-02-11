"""
Phase 2: Symptom Neglect & Underreporting Detection
=====================================================
Detects when users minimize serious symptoms.
"""

from app.engine.knowledge_base import (
    MINIMIZATION_PHRASES,
    ALWAYS_HIGH_SYMPTOMS,
    MEDIUM_SYMPTOMS,
    SYMPTOM_SYNONYMS,
)


def detect_neglect(raw_text: str, normalized_symptoms: list[str]) -> dict:
    """
    Detect if user is minimizing or downplaying serious symptoms.

    Returns:
        {
            "neglect_detected": "Yes" | "No",
            "neglect_reason": str
        }
    """
    if not raw_text:
        return {"neglect_detected": "No", "neglect_reason": ""}

    text_lower = raw_text.lower()
    reasons = []

    # 1. Check for minimization phrases
    found_phrases = [p for p in MINIMIZATION_PHRASES if p in text_lower]

    # 2. Check if minimization co-occurs with high-risk symptoms
    has_high_risk = any(s in ALWAYS_HIGH_SYMPTOMS for s in normalized_symptoms)
    has_medium_risk = any(s in MEDIUM_SYMPTOMS for s in normalized_symptoms)

    # Also check via synonym mapping
    for phrase, normalized in SYMPTOM_SYNONYMS.items():
        if phrase in text_lower:
            if normalized in ALWAYS_HIGH_SYMPTOMS:
                has_high_risk = True
            elif normalized in MEDIUM_SYMPTOMS:
                has_medium_risk = True

    if found_phrases and has_high_risk:
        phrases_str = ", ".join(f'"{p}"' for p in found_phrases)
        reasons.append(
            f"You used minimizing language ({phrases_str}) while describing "
            f"symptoms that can sometimes be associated with serious conditions. "
            f"It's important to take these symptoms seriously."
        )

    if found_phrases and has_medium_risk and not has_high_risk:
        phrases_str = ", ".join(f'"{p}"' for p in found_phrases)
        reasons.append(
            f"You used words like {phrases_str} when describing your symptoms. "
            f"These symptoms may benefit from professional evaluation even if "
            f"they feel mild right now."
        )

    # 3. Check for contradiction patterns (e.g., "chest pain" + "not serious")
    contradiction_pairs = [
        ("chest pain", ["not serious", "no big deal", "it's fine", "nothing"]),
        ("breathing", ["just", "a little", "minor", "slight"]),
        ("fainting", ["just", "only", "once"]),
        ("slurred speech", ["a little", "minor"]),
    ]

    for symptom_phrase, minimizers in contradiction_pairs:
        if symptom_phrase in text_lower:
            for m in minimizers:
                if m in text_lower:
                    reasons.append(
                        f'You mentioned "{symptom_phrase}" but also said "{m}". '
                        f"This symptom deserves careful attention regardless of "
                        f"how mild it may feel."
                    )
                    break  # One reason per symptom phrase

    if reasons:
        return {
            "neglect_detected": "Yes",
            "neglect_reason": " ".join(reasons),
        }

    return {"neglect_detected": "No", "neglect_reason": ""}
