"""
Phase 8: Family / Caregiver Escalation Logic
==============================================
Suggests involving a trusted person for high-risk cases.
"""


def evaluate_caregiver_alert(risk_level: str, age: int | None = None) -> dict:
    """
    Determine if caregiver involvement should be suggested.

    Returns:
        {
            "caregiver_alert_suggestion": "Yes" | "No",
            "caregiver_reason": str
        }
    """
    if risk_level == "High":
        reason = (
            "Given the urgency of your symptoms, we strongly recommend "
            "informing a trusted family member, friend, or caregiver. "
            "Having someone aware of your situation can help ensure you "
            "receive timely assistance, especially if symptoms worsen."
        )

        if age and age >= 60:
            reason += (
                " This is particularly important for individuals above 60, "
                "where prompt support can make a significant difference."
            )

        return {
            "caregiver_alert_suggestion": "Yes",
            "caregiver_reason": reason,
        }

    if risk_level == "Medium" and age and age >= 65:
        return {
            "caregiver_alert_suggestion": "Yes",
            "caregiver_reason": (
                "As a precaution, it may be helpful to let a family member "
                "or caregiver know about your symptoms so they can assist "
                "with your doctor's visit if needed."
            ),
        }

    return {
        "caregiver_alert_suggestion": "No",
        "caregiver_reason": "",
    }
