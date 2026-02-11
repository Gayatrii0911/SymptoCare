"""
Data models for the Health Triage Copilot.
Plain Python classes – no ORM needed for the MVP.
"""


class UserProfile:
    def __init__(self, age: int = None, gender: str = None):
        self.age = age
        self.gender = gender

    def to_dict(self):
        return {"age": self.age, "gender": self.gender}


class TriageInput:
    """Encapsulates everything captured in Phase 1."""

    def __init__(
        self,
        raw_symptoms: str,
        normalized_symptoms: list[str],
        user_profile: UserProfile,
        input_language: str = "en",
        input_method: str = "text",
    ):
        self.raw_symptoms = raw_symptoms
        self.normalized_symptoms = normalized_symptoms
        self.user_profile = user_profile
        self.input_language = input_language
        self.input_method = input_method

    def to_dict(self):
        return {
            "raw_symptoms": self.raw_symptoms,
            "normalized_symptoms": self.normalized_symptoms,
            "user_profile": self.user_profile.to_dict(),
            "input_language": self.input_language,
            "input_method": self.input_method,
        }


class TriageResult:
    """Final output structure returned by the pipeline."""

    def __init__(
        self,
        risk_level: str = "Low",
        confidence_band: str = "low",
        explanation: str = "",
        neglect_detected: str = "No",
        neglect_reason: str = "",
        silent_emergency_flag: str = "Low",
        risk_pattern_explanation: str = "",
        what_if_ignored: str = "",
        recommended_action: str = "",
        caregiver_alert_suggestion: str = "No",
        caregiver_reason: str = "",
        language: str = "en",
    ):
        self.risk_level = risk_level
        self.confidence_band = confidence_band
        self.explanation = explanation
        self.neglect_detected = neglect_detected
        self.neglect_reason = neglect_reason
        self.silent_emergency_flag = silent_emergency_flag
        self.risk_pattern_explanation = risk_pattern_explanation
        self.what_if_ignored = what_if_ignored
        self.recommended_action = recommended_action
        self.caregiver_alert_suggestion = caregiver_alert_suggestion
        self.caregiver_reason = caregiver_reason
        self.language = language

    def to_dict(self):
        return {
            "risk_level": self.risk_level,
            "confidence_band": self.confidence_band,
            "explanation": self.explanation,
            "neglect_detected": self.neglect_detected,
            "neglect_reason": self.neglect_reason,
            "silent_emergency_flag": self.silent_emergency_flag,
            "risk_pattern_explanation": self.risk_pattern_explanation,
            "what_if_ignored": self.what_if_ignored,
            "recommended_action": self.recommended_action,
            "caregiver_alert_suggestion": self.caregiver_alert_suggestion,
            "caregiver_reason": self.caregiver_reason,
            "language": self.language,
        }
