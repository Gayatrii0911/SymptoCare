"""
API Routes for the Health Triage Copilot
"""

from flask import Blueprint, request, jsonify
from app.engine.pipeline import run_triage
from ml.predictor import get_all_symptoms, get_severity_map, get_disease_info

api_bp = Blueprint("api", __name__)


@api_bp.route("/")
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "Avalon backend running",
        "version": "1.0.0",
        "service": "AI Health Triage Copilot",
    })


@api_bp.route("/triage", methods=["POST"])
def triage():
    """
    Main triage endpoint.

    Accepts JSON:
        {
            "age": int,
            "gender": str,
            "symptoms": list[str] | str,
            "raw_text": str (optional),
            "input_method": "text" | "voice",
            "language": "en" | "hi" | "mr"
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate minimum input
        symptoms = data.get("symptoms", [])
        raw_text = data.get("raw_text", "")
        if not symptoms and not raw_text:
            return jsonify({"error": "Please provide symptoms or raw_text"}), 400

        result = run_triage(data)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": "An internal error occurred",
            "detail": str(e),
        }), 500


@api_bp.route("/symptoms", methods=["GET"])
def get_symptoms():
    """Return all available symptoms grouped by severity."""
    all_symptoms = get_all_symptoms()
    severity_map = get_severity_map()

    # Group by severity weight
    categorized = {
        "critical": [],     # weight >= 6
        "high": [],         # weight 4-5
        "moderate": [],     # weight 3
        "mild": [],         # weight 1-2
    }

    for symptom in all_symptoms:
        weight = severity_map.get(symptom.lower(), 1)
        readable = symptom.replace("_", " ").title()
        entry = {"id": symptom, "name": readable, "weight": weight}

        if weight >= 6:
            categorized["critical"].append(entry)
        elif weight >= 4:
            categorized["high"].append(entry)
        elif weight >= 3:
            categorized["moderate"].append(entry)
        else:
            categorized["mild"].append(entry)

    return jsonify({
        "symptoms": [
            {"id": s, "name": s.replace("_", " ").title()}
            for s in all_symptoms
        ],
        "categorized": categorized,
        "total": len(all_symptoms),
    })


@api_bp.route("/diseases", methods=["GET"])
def get_diseases():
    """Return all diseases with descriptions and severity tiers."""
    disease_info = get_disease_info()

    diseases = []
    for name, info in sorted(disease_info.items()):
        diseases.append({
            "name": name,
            "description": info.get("description", ""),
            "severity_tier": info.get("severity_tier", "Low"),
            "precautions": info.get("precautions", []),
        })

    return jsonify({
        "diseases": diseases,
        "total": len(diseases),
    })
