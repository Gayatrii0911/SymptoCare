"""
Phase 5: Explainability-First Risk Narratives
===============================================
Generates human-readable explanations in 3 sections.
"""


def generate_explanation(
    normalized_symptoms: list[str],
    risk_level: str,
    neglect_detected: str,
    neglect_reason: str,
    silent_risk_flag: str,
    risk_pattern_explanation: str,
    ml_prediction: dict | None,
    age: int | None = None,
    gender: str | None = None,
) -> dict:
    """
    Build a 3-part explanation:
      - "What we noticed"
      - "Why it matters"
      - "What this means for you"

    Returns: dict with the 3 keys.
    """
    # ── What we noticed ─────────────────────────────────────────────────
    symptom_names = [s.replace("_", " ") for s in normalized_symptoms]
    noticed_parts = []

    if symptom_names:
        noticed_parts.append(
            f"You reported the following symptoms: {', '.join(symptom_names)}."
        )

    if age:
        noticed_parts.append(f"Your age is {age}.")

    if neglect_detected == "Yes":
        noticed_parts.append(
            "We also noticed that the way you described your symptoms "
            "may be underestimating their significance."
        )

    what_we_noticed = " ".join(noticed_parts) if noticed_parts else "No symptoms were reported."

    # ── Why it matters ──────────────────────────────────────────────────
    matters_parts = []

    if risk_pattern_explanation:
        matters_parts.append(risk_pattern_explanation)

    if ml_prediction:
        disease = ml_prediction.get("predicted_disease", "")
        confidence = ml_prediction.get("confidence", 0)
        description = ml_prediction.get("disease_description", "")
        if disease and confidence >= 0.5:
            matters_parts.append(
                f"Based on your symptom pattern, this can sometimes be "
                f"associated with conditions like {disease}."
            )
            if description:
                matters_parts.append(description)

    if neglect_reason:
        matters_parts.append(neglect_reason)

    if not matters_parts:
        if risk_level == "Low":
            matters_parts.append(
                "Your symptoms appear to be mild based on the patterns we analyzed."
            )
        elif risk_level == "Medium":
            matters_parts.append(
                "Some of your symptoms may benefit from professional evaluation."
            )
        else:
            matters_parts.append(
                "The combination of symptoms you described can sometimes "
                "be associated with conditions that need prompt attention."
            )

    why_it_matters = " ".join(matters_parts)

    # ── What this means for you ─────────────────────────────────────────
    if risk_level == "High":
        what_this_means = (
            "Based on the overall pattern, we recommend seeking medical "
            "attention as soon as possible. This is a precautionary recommendation, "
            "not a diagnosis."
        )
    elif risk_level == "Medium":
        what_this_means = (
            "We recommend consulting a healthcare professional within the "
            "next 24-48 hours. In the meantime, monitor your symptoms closely "
            "and seek immediate care if they worsen."
        )
    else:
        what_this_means = (
            "Your symptoms appear manageable with self-care for now. "
            "However, if symptoms persist or worsen, please consult a "
            "healthcare professional."
        )

    return {
        "what_we_noticed": what_we_noticed,
        "why_it_matters": why_it_matters,
        "what_this_means": what_this_means,
    }
