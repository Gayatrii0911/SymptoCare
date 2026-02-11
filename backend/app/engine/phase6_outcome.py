"""
Phase 6: Outcome Awareness – "What if I ignore this?"
=======================================================
Bridges risk awareness → action ethically.
"""


def generate_outcome_awareness(
    risk_level: str,
    normalized_symptoms: list[str],
    ml_prediction: dict | None = None,
) -> dict:
    """
    Describe possible consequences of delaying care.

    Returns:
        {
            "short_term": str,
            "long_term": str
        }
    """
    severity_tier = ""
    if ml_prediction:
        severity_tier = ml_prediction.get("severity_tier", "Low")

    symptom_set = set(normalized_symptoms)

    # ── High Risk ───────────────────────────────────────────────────────
    if risk_level == "High":
        short_term = (
            "In some cases, delaying care for these symptoms could lead to "
            "rapid worsening. Conditions associated with these patterns "
            "may progress quickly and benefit greatly from early intervention."
        )

        if "chest_pain" in symptom_set or "breathlessness" in symptom_set:
            short_term += (
                " Chest-related symptoms in particular may indicate "
                "time-sensitive conditions where every hour matters."
            )

        long_term = (
            "Over time, untreated symptoms of this severity could potentially "
            "lead to complications that are harder to manage. Early detection "
            "and treatment generally lead to better outcomes."
        )

    # ── Medium Risk ─────────────────────────────────────────────────────
    elif risk_level == "Medium":
        short_term = (
            "If left unattended, these symptoms may persist or gradually "
            "worsen over the next few days. Some conditions start mild but "
            "can escalate if not properly evaluated."
        )
        long_term = (
            "Prolonged neglect of these symptoms could potentially lead to "
            "chronic issues or complications. A timely check-up can help "
            "prevent this."
        )

    # ── Low Risk ────────────────────────────────────────────────────────
    else:
        short_term = (
            "These symptoms are generally self-limiting and may improve "
            "with rest and basic self-care within a few days."
        )
        long_term = (
            "If symptoms persist beyond a week or new symptoms develop, "
            "it would be wise to consult a healthcare professional to rule "
            "out any underlying causes."
        )

    return {
        "short_term": short_term,
        "long_term": long_term,
    }
