"""
Phase 4: Risk Level Classification
====================================
Combines ML prediction + rule-based assessment + neglect/silent flags
to produce a final risk level.
"""

from app.engine.knowledge_base import (
    HIGH_RISK_CLUSTERS,
    ALWAYS_HIGH_SYMPTOMS,
    MEDIUM_SYMPTOMS,
    LOW_SYMPTOMS,
)
from ml.predictor import predict_disease, get_symptom_severity


def classify_risk(
    normalized_symptoms: list[str],
    neglect_detected: str,
    silent_risk_flag: str,
) -> dict:
    """
    Combine all signals to assign a risk level.

    Returns:
        {
            "risk_level": "Low" | "Medium" | "High",
            "confidence_band": "low" | "moderate" | "high",
            "ml_prediction": dict (from ML predictor),
        }
    """
    if not normalized_symptoms:
        return {
            "risk_level": "Low",
            "confidence_band": "low",
            "ml_prediction": None,
        }

    # ── 1. ML Prediction ────────────────────────────────────────────────
    ml_result = predict_disease(normalized_symptoms)
    ml_severity = ml_result.get("severity_tier", "Low")
    ml_confidence = ml_result.get("confidence", 0)

    # ── 2. Rule-based symptom severity ──────────────────────────────────
    symptom_set = set(normalized_symptoms)
    rule_risk = "Low"

    # Check individual symptom severity
    if symptom_set & ALWAYS_HIGH_SYMPTOMS:
        rule_risk = "High"
    elif symptom_set & MEDIUM_SYMPTOMS:
        rule_risk = "Medium"

    # Check cluster matches
    for cluster_symptoms, cluster_severity, _ in HIGH_RISK_CLUSTERS:
        if cluster_symptoms.issubset(symptom_set):
            if _severity_rank(cluster_severity) > _severity_rank(rule_risk):
                rule_risk = cluster_severity

    # ── 3. Weighted severity score from symptom weights ─────────────────
    total_weight = sum(get_symptom_severity(s) for s in normalized_symptoms)
    avg_weight = total_weight / len(normalized_symptoms) if normalized_symptoms else 0

    if avg_weight >= 5:
        weight_risk = "High"
    elif avg_weight >= 3:
        weight_risk = "Medium"
    else:
        weight_risk = "Low"

    # ── 4. Combine all signals ──────────────────────────────────────────
    signals = [
        rule_risk,
        weight_risk,
        silent_risk_flag if silent_risk_flag != "Moderate" else "Medium",
    ]

    # ML prediction contributes if confidence is reasonable
    if ml_confidence >= 0.5:
        signals.append(ml_severity)

    # Neglect escalation
    if neglect_detected == "Yes":
        # Bump Low → Medium, Medium → High
        signals = [_escalate(s) for s in signals]

    # Final risk = highest signal
    final_risk = max(signals, key=_severity_rank)

    # ── 5. Confidence band ──────────────────────────────────────────────
    # Based on agreement between signals
    risk_counts = {}
    for s in signals:
        risk_counts[s] = risk_counts.get(s, 0) + 1

    agreement = risk_counts.get(final_risk, 0) / len(signals)
    if agreement >= 0.75:
        confidence_band = "high"
    elif agreement >= 0.5:
        confidence_band = "moderate"
    else:
        confidence_band = "low"

    return {
        "risk_level": final_risk,
        "confidence_band": confidence_band,
        "ml_prediction": ml_result,
    }


def _severity_rank(level: str) -> int:
    return {"Low": 0, "Moderate": 1, "Medium": 1, "High": 2}.get(level, 0)


def _escalate(level: str) -> str:
    return {"Low": "Medium", "Medium": "High", "High": "High"}.get(level, level)
