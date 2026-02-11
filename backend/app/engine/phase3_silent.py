"""
Phase 3: Silent / Atypical Emergency Detection
================================================
Catches dangerous but subtle symptom patterns often missed by users.
"""

from app.engine.knowledge_base import SILENT_EMERGENCY_PATTERNS


def detect_silent_emergency(
    normalized_symptoms: list[str],
    age: int | None = None,
    gender: str | None = None,
) -> dict:
    """
    Check for symptom clusters linked to high-mortality conditions
    with mild presentation.

    Returns:
        {
            "silent_risk_flag": "Low" | "Moderate" | "High",
            "risk_pattern_explanation": str
        }
    """
    symptom_set = set(normalized_symptoms)
    highest_flag = "Low"
    explanations = []

    flag_rank = {"Low": 0, "Moderate": 1, "High": 2}

    for pattern in SILENT_EMERGENCY_PATTERNS:
        required_symptoms = pattern["symptoms"]
        age_min = pattern.get("age_min")
        gender_req = pattern.get("gender")
        flag = pattern["flag"]
        explanation = pattern["explanation"]

        # Check symptom match
        if not required_symptoms.issubset(symptom_set):
            continue

        # Check age modifier
        if age_min is not None:
            if age is None or age < age_min:
                continue

        # Check gender modifier
        if gender_req is not None:
            if gender is None or gender.lower() != gender_req.lower():
                continue

        # Pattern matched
        if flag_rank.get(flag, 0) > flag_rank.get(highest_flag, 0):
            highest_flag = flag

        explanations.append(explanation)

    return {
        "silent_risk_flag": highest_flag,
        "risk_pattern_explanation": " ".join(explanations) if explanations else "",
    }
