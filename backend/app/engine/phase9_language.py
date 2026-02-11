"""
Phase 9: Multilingual & Voice-Aware Response
==============================================
Translates key response fields into user's language.
Keeps sentences short and voice-friendly.
Includes medical keyword translations.
"""

import re
from app.engine.translations import (
    translate_disease_name,
    translate_symptom,
    translate_full_text,
    translate_symptom_in_text,
    DISEASE_NAMES,
    SYMPTOM_TRANSLATIONS,
)

# ── Translation dictionaries ────────────────────────────────────────────────
# Only key UI-facing phrases are translated. Full translation would
# require a proper i18n service; this is a rule-based MVP approach.

TRANSLATIONS = {
    "hi": {
        # Risk levels
        "Low": "कम",
        "Medium": "मध्यम",
        "High": "उच्च",
        # Confidence
        "low": "कम",
        "moderate": "मध्यम",
        "high": "उच्च",
        # Neglect
        "Yes": "हाँ",
        "No": "नहीं",
        # Caregiver
        "disclaimer": (
            "⚕️ महत्वपूर्ण: यह कोई चिकित्सा निदान नहीं है। "
            "कृपया उचित मूल्यांकन के लिए योग्य चिकित्सक से परामर्श करें।"
        ),
        # Action headers
        "IMMEDIATE ACTION RECOMMENDED": "तुरंत कार्रवाई की सिफारिश",
        "CONSULTATION RECOMMENDED": "परामर्श की सिफारिश",
        "SELF-CARE GUIDANCE": "स्व-देखभाल मार्गदर्शन",
        # Explanation headers
        "What we noticed": "हमने क्या देखा",
        "Why it matters": "यह क्यों मायने रखता है",
        "What this means for you": "आपके लिए इसका क्या मतलब है",
    },
    "mr": {
        # Risk levels
        "Low": "कमी",
        "Medium": "मध्यम",
        "High": "उच्च",
        # Confidence
        "low": "कमी",
        "moderate": "मध्यम",
        "high": "उच्च",
        # Neglect
        "Yes": "होय",
        "No": "नाही",
        # Caregiver
        "disclaimer": (
            "⚕️ महत्त्वाचे: हे वैद्यकीय निदान नाही. "
            "कृपया योग्य मूल्यांकनासाठी पात्र डॉक्टरांचा सल्ला घ्या."
        ),
        # Action headers
        "IMMEDIATE ACTION RECOMMENDED": "तात्काळ कारवाई आवश्यक",
        "CONSULTATION RECOMMENDED": "डॉक्टरांचा सल्ला घ्या",
        "SELF-CARE GUIDANCE": "स्वत:ची काळजी घ्या",
        # Explanation headers
        "What we noticed": "आम्हाला काय आढळले",
        "Why it matters": "हे का महत्त्वाचे आहे",
        "What this means for you": "तुमच्यासाठी याचा अर्थ काय",
    },
}


def localize_response(response: dict, language: str) -> dict:
    """
    Translate key fields in the response dict to the target language.
    English responses are returned as-is.
    Translates disease names, symptoms, descriptions, and all medical keywords.
    """
    if language == "en" or language not in TRANSLATIONS:
        return response

    t = TRANSLATIONS[language]
    localized = response.copy()

    # ── Translate simple fields ──────────────────────────────────────────────
    if "risk_level" in localized:
        localized["risk_level"] = t.get(localized["risk_level"], localized["risk_level"])

    if "confidence_band" in localized:
        localized["confidence_band"] = t.get(
            localized["confidence_band"], localized["confidence_band"]
        )

    if "neglect_detected" in localized:
        localized["neglect_detected"] = t.get(
            localized["neglect_detected"], localized["neglect_detected"]
        )

    if "caregiver_alert_suggestion" in localized:
        localized["caregiver_alert_suggestion"] = t.get(
            localized["caregiver_alert_suggestion"],
            localized["caregiver_alert_suggestion"],
        )

    if "silent_emergency_flag" in localized:
        localized["silent_emergency_flag"] = t.get(
            localized["silent_emergency_flag"],
            localized["silent_emergency_flag"],
        )

    if "disclaimer" in localized:
        localized["disclaimer"] = t.get("disclaimer", localized["disclaimer"])

    # ── Translate disease names ───────────────────────────────────────────────
    if "predicted_condition" in localized and localized["predicted_condition"]:
        localized["predicted_condition"] = translate_disease_name(
            localized["predicted_condition"], language
        )

    # ── Translate top 3 conditions ────────────────────────────────────────────
    if "top_3_conditions" in localized and localized["top_3_conditions"]:
        localized["top_3_conditions"] = [
            (translate_disease_name(disease, language), prob)
            for disease, prob in localized["top_3_conditions"]
        ]

    # ── Translate explanations ───────────────────────────────────────────────
    if "explanation" in localized and isinstance(localized["explanation"], dict):
        explanation = localized["explanation"]
        if "what_we_noticed" in explanation:
            explanation["what_we_noticed"] = translate_full_text(
                explanation["what_we_noticed"], language
            )
        if "why_it_matters" in explanation:
            explanation["why_it_matters"] = translate_full_text(
                explanation["why_it_matters"], language
            )
        if "what_this_means" in explanation:
            explanation["what_this_means"] = translate_full_text(
                explanation["what_this_means"], language
            )

    # ── Translate risk pattern explanation ────────────────────────────────────
    if "risk_pattern_explanation" in localized:
        localized["risk_pattern_explanation"] = translate_full_text(
            localized["risk_pattern_explanation"], language
        )

    # ── Translate neglect reason ──────────────────────────────────────────────
    if "neglect_reason" in localized:
        localized["neglect_reason"] = translate_full_text(
            localized["neglect_reason"], language
        )

    # ── Translate caregiver reason ────────────────────────────────────────────
    if "caregiver_reason" in localized:
        localized["caregiver_reason"] = translate_full_text(
            localized["caregiver_reason"], language
        )

    # ── Translate what_if_ignored ────────────────────────────────────────────
    if "what_if_ignored" in localized and isinstance(localized["what_if_ignored"], dict):
        if "short_term" in localized["what_if_ignored"]:
            localized["what_if_ignored"]["short_term"] = translate_full_text(
                localized["what_if_ignored"]["short_term"], language
            )
        if "long_term" in localized["what_if_ignored"]:
            localized["what_if_ignored"]["long_term"] = translate_full_text(
                localized["what_if_ignored"]["long_term"], language
            )

    # ── Translate recommended action ──────────────────────────────────────────
    if "recommended_action" in localized:
        localized["recommended_action"] = translate_full_text(
            localized["recommended_action"], language
        )

    # ── Translate NLP extracted symptoms ──────────────────────────────────────
    if "nlp" in localized and isinstance(localized["nlp"], dict):
        if "extracted_symptoms" in localized["nlp"]:
            localized["nlp"]["extracted_symptoms"] = [
                translate_symptom(symptom, language)
                for symptom in localized["nlp"]["extracted_symptoms"]
            ]
        if "negated_symptoms" in localized["nlp"]:
            localized["nlp"]["negated_symptoms"] = [
                translate_symptom(symptom, language)
                for symptom in localized["nlp"]["negated_symptoms"]
            ]

    # ── Translate input summary ───────────────────────────────────────────────
    if "input_summary" in localized and isinstance(localized["input_summary"], dict):
        if "normalized_symptoms" in localized["input_summary"]:
            localized["input_summary"]["normalized_symptoms"] = [
                translate_symptom(symptom, language)
                for symptom in localized["input_summary"]["normalized_symptoms"]
            ]

    return localized
