"""
Triage Pipeline – Orchestrator
================================
Runs Phase 1 → Phase 9 sequentially and builds the final TriageResult.
"""

from app.models import TriageInput, TriageResult
from app.engine.phase1_input import process_input
from app.engine.phase2_neglect import detect_neglect
from app.engine.phase3_silent import detect_silent_emergency
from app.engine.phase4_risk import classify_risk
from app.engine.phase5_explain import generate_explanation
from app.engine.phase6_outcome import generate_outcome_awareness
from app.engine.phase7_action import generate_recommendations
from app.engine.phase8_caregiver import evaluate_caregiver_alert
from app.engine.phase9_language import localize_response


def run_triage(data: dict) -> dict:
    """
    Execute the full triage pipeline.

    Args:
        data: Raw request dict with age, gender, symptoms, etc.

    Returns:
        Final response dict ready for JSON serialization.
    """

    # ── Phase 1: Input Parsing ──────────────────────────────────────────
    triage_input: TriageInput = process_input(data)

    if not triage_input.normalized_symptoms:
        return {
            "risk_level": "Low",
            "confidence_band": "low",
            "explanation": {
                "what_we_noticed": "No recognizable symptoms were provided.",
                "why_it_matters": "We could not perform a meaningful assessment.",
                "what_this_means": "Please try again with specific symptoms.",
            },
            "neglect_detected": "No",
            "neglect_reason": "",
            "silent_emergency_flag": "Low",
            "risk_pattern_explanation": "",
            "what_if_ignored": {"short_term": "", "long_term": ""},
            "recommended_action": "Please provide your symptoms for assessment.",
            "predicted_condition": "",
            "ml_confidence": 0,
            "top_3_conditions": [],
            "caregiver_alert_suggestion": "No",
            "caregiver_reason": "",
            "language": triage_input.input_language,
            "input_summary": triage_input.to_dict(),
            "disclaimer": "This is not a medical diagnosis. Please consult a healthcare professional.",
        }

    # ── Phase 2: Neglect Detection ──────────────────────────────────────
    neglect = detect_neglect(
        triage_input.raw_symptoms,
        triage_input.normalized_symptoms,
    )

    # ── Phase 3: Silent Emergency Detection ─────────────────────────────
    silent = detect_silent_emergency(
        triage_input.normalized_symptoms,
        age=triage_input.user_profile.age,
        gender=triage_input.user_profile.gender,
    )

    # ── Phase 4: Risk Classification ────────────────────────────────────
    risk = classify_risk(
        triage_input.normalized_symptoms,
        neglect["neglect_detected"],
        silent["silent_risk_flag"],
    )

    ml_prediction = risk.get("ml_prediction")

    # ── Phase 5: Explainability ─────────────────────────────────────────
    explanation = generate_explanation(
        triage_input.normalized_symptoms,
        risk["risk_level"],
        neglect["neglect_detected"],
        neglect["neglect_reason"],
        silent["silent_risk_flag"],
        silent["risk_pattern_explanation"],
        ml_prediction,
        age=triage_input.user_profile.age,
        gender=triage_input.user_profile.gender,
    )

    # ── Phase 6: Outcome Awareness ──────────────────────────────────────
    outcome = generate_outcome_awareness(
        risk["risk_level"],
        triage_input.normalized_symptoms,
        ml_prediction,
    )

    # ── Phase 7: Recommendations ────────────────────────────────────────
    action = generate_recommendations(
        risk["risk_level"],
        ml_prediction,
    )

    # ── Phase 8: Caregiver Escalation ───────────────────────────────────
    caregiver = evaluate_caregiver_alert(
        risk["risk_level"],
        age=triage_input.user_profile.age,
    )

    # ── Build response ──────────────────────────────────────────────────
    # NLP metadata
    negated = getattr(triage_input, '_negated_symptoms', [])

    response = {
        "risk_level": risk["risk_level"],
        "confidence_band": risk["confidence_band"],
        "explanation": explanation,
        "neglect_detected": neglect["neglect_detected"],
        "neglect_reason": neglect["neglect_reason"],
        "silent_emergency_flag": silent["silent_risk_flag"],
        "risk_pattern_explanation": silent["risk_pattern_explanation"],
        "what_if_ignored": outcome,
        "recommended_action": action,
        "predicted_condition": ml_prediction.get("predicted_disease", "") if ml_prediction else "",
        "ml_confidence": ml_prediction.get("confidence", 0) if ml_prediction else 0,
        "top_3_conditions": ml_prediction.get("top_3", []) if ml_prediction else [],
        "caregiver_alert_suggestion": caregiver["caregiver_alert_suggestion"],
        "caregiver_reason": caregiver["caregiver_reason"],
        "language": triage_input.input_language,
        "input_summary": triage_input.to_dict(),
        "nlp": {
            "extracted_symptoms": triage_input.normalized_symptoms,
            "negated_symptoms": negated,
            "symptom_count": len(triage_input.normalized_symptoms),
        },
        "disclaimer": "This is not a medical diagnosis. Please consult a healthcare professional.",
    }

    # ── Phase 9: Multilingual ───────────────────────────────────────────
    response = localize_response(response, triage_input.input_language)

    return response
