"""
Phase 7: Actionable Recommendations
=====================================
Tells the user what to do next based on risk level.
"""


def generate_recommendations(
    risk_level: str,
    ml_prediction: dict | None = None,
) -> str:
    """
    Generate actionable next steps.

    Returns: recommendation string
    """
    precautions = []
    if ml_prediction:
        precautions = ml_prediction.get("precautions", [])

    parts = []

    if risk_level == "High":
        parts.append(
            "⚠️ IMMEDIATE ACTION RECOMMENDED:\n"
            "• Please seek medical attention as soon as possible.\n"
            "• Visit the nearest hospital or call emergency services.\n"
            "• Do not drive yourself — ask someone to take you or call an ambulance.\n"
            "• Stay calm and avoid physical exertion until you receive medical help."
        )

    elif risk_level == "Medium":
        parts.append(
            "📋 CONSULTATION RECOMMENDED:\n"
            "• Schedule a doctor's appointment within the next 24-48 hours.\n"
            "• Monitor your symptoms closely — note any changes.\n"
            "• Seek immediate care if symptoms suddenly worsen."
        )
        parts.append(
            "\n🔍 WARNING SIGNS TO WATCH:\n"
            "• Sudden increase in severity\n"
            "• New symptoms appearing (especially difficulty breathing, "
            "chest pain, or confusion)\n"
            "• Symptoms not improving after 48 hours"
        )

    else:  # Low
        parts.append(
            "🟢 SELF-CARE GUIDANCE:\n"
            "• Get adequate rest and stay hydrated.\n"
            "• Monitor your symptoms over the next few days.\n"
            "• Use over-the-counter remedies only as directed.\n"
            "• Consult a doctor if symptoms persist beyond a week."
        )

    # Add disease-specific precautions from dataset
    if precautions:
        prec_list = "\n".join(f"• {p.strip().capitalize()}" for p in precautions if p)
        parts.append(f"\n📌 SPECIFIC PRECAUTIONS:\n{prec_list}")

    # Always add disclaimer
    parts.append(
        "\n⚕️ IMPORTANT: This is not a medical diagnosis. "
        "Please consult a qualified healthcare professional for proper evaluation."
    )

    return "\n".join(parts)
