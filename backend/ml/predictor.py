"""
ML Predictor – loads trained model artifacts and provides prediction API.
"""

import os
import pickle
import numpy as np

ML_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Lazy-loaded singletons ───────────────────────────────────────────────────
_model = None
_label_encoder = None
_symptom_columns = None
_severity_map = None
_disease_info = None


def _load(filename):
    path = os.path.join(ML_DIR, filename)
    with open(path, "rb") as f:
        return pickle.load(f)


def get_model():
    global _model
    if _model is None:
        _model = _load("model.pkl")
    return _model


def get_label_encoder():
    global _label_encoder
    if _label_encoder is None:
        _label_encoder = _load("label_encoder.pkl")
    return _label_encoder


def get_symptom_columns() -> list[str]:
    global _symptom_columns
    if _symptom_columns is None:
        _symptom_columns = _load("symptom_columns.pkl")
    return _symptom_columns


def get_severity_map() -> dict[str, int]:
    global _severity_map
    if _severity_map is None:
        _severity_map = _load("severity_map.pkl")
    return _severity_map


def get_disease_info() -> dict:
    global _disease_info
    if _disease_info is None:
        _disease_info = _load("disease_info.pkl")
    return _disease_info


def predict_disease(symptoms: list[str]) -> dict:
    """
    Given a list of normalized symptom names, predict the disease.

    Returns:
        {
            "predicted_disease": str,
            "confidence": float (0-1),
            "top_3": [(disease, probability), ...],
            "disease_description": str,
            "precautions": [str, ...],
            "severity_tier": "Low" | "Medium" | "High",
        }
    """
    model = get_model()
    le = get_label_encoder()
    columns = get_symptom_columns()
    disease_db = get_disease_info()

    # Build binary feature vector
    feature_vector = np.zeros((1, len(columns)), dtype=int)
    col_index = {s: i for i, s in enumerate(columns)}
    for symptom in symptoms:
        s = symptom.strip().lower()
        if s in col_index:
            feature_vector[0, col_index[s]] = 1

    # Predict
    prediction = model.predict(feature_vector)[0]
    disease_name = le.inverse_transform([prediction])[0]

    # Probabilities (top 3)
    if hasattr(model, "predict_proba"):
        probas = model.predict_proba(feature_vector)[0]
        top_indices = np.argsort(probas)[::-1][:3]
        top_3 = [
            (le.inverse_transform([i])[0], round(float(probas[i]), 4))
            for i in top_indices
        ]
        confidence = float(probas[prediction])
    else:
        top_3 = [(disease_name, 1.0)]
        confidence = 1.0

    # Disease info
    info = disease_db.get(disease_name, {})

    return {
        "predicted_disease": disease_name,
        "confidence": round(confidence, 4),
        "top_3": top_3,
        "disease_description": info.get("description", ""),
        "precautions": info.get("precautions", []),
        "severity_tier": info.get("severity_tier", "Low"),
    }


def get_all_symptoms() -> list[str]:
    """Return all symptom names the model was trained on."""
    return get_symptom_columns()


def get_symptom_severity(symptom: str) -> int:
    """Return severity weight for a symptom (default 1)."""
    smap = get_severity_map()
    return smap.get(symptom.strip().lower(), 1)
