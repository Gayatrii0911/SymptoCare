"""
Comprehensive Test Suite for Health Triage Copilot
===================================================
Tests ML model accuracy, all pipeline phases, and API endpoints.
"""

import os
import sys
import json
import pickle
import unittest

import numpy as np
import pandas as pd

# Add backend root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.predictor import predict_disease, get_all_symptoms, get_symptom_severity, get_disease_info
from app.engine.phase1_input import process_input, normalize_symptoms_from_text, detect_language
from app.engine.nlp import extract_symptoms_nlp
from app.engine.phase2_neglect import detect_neglect
from app.engine.phase3_silent import detect_silent_emergency
from app.engine.phase4_risk import classify_risk
from app.engine.phase5_explain import generate_explanation
from app.engine.phase6_outcome import generate_outcome_awareness
from app.engine.phase7_action import generate_recommendations
from app.engine.phase8_caregiver import evaluate_caregiver_alert
from app.engine.phase9_language import localize_response
from app.engine.pipeline import run_triage
from app import create_app


class TestMLModel(unittest.TestCase):
    """Test ML model predictions and accuracy."""

    def test_model_loads(self):
        """Model and artifacts load without error."""
        symptoms = get_all_symptoms()
        self.assertEqual(len(symptoms), 131)

    def test_predict_heart_attack(self):
        """Chest pain + sweating + breathlessness → Heart attack."""
        result = predict_disease(["chest_pain", "breathlessness", "sweating"])
        self.assertEqual(result["predicted_disease"], "Heart attack")
        self.assertGreater(result["confidence"], 0.5)
        self.assertEqual(result["severity_tier"], "High")

    def test_predict_common_cold(self):
        """Cough + runny nose + sneezing → Common Cold."""
        result = predict_disease(["continuous_sneezing", "cough", "headache", "chills"])
        self.assertIn(result["predicted_disease"], ["Common Cold", "Allergy"])

    def test_predict_malaria(self):
        """High fever + chills + vomiting + sweating → Malaria."""
        result = predict_disease(["high_fever", "chills", "vomiting", "sweating", "headache", "nausea", "muscle_pain"])
        self.assertEqual(result["predicted_disease"], "Malaria")
        self.assertGreater(result["confidence"], 0.5)

    def test_predict_dengue(self):
        """Dengue symptom cluster."""
        result = predict_disease(["skin_rash", "chills", "joint_pain", "vomiting", "fatigue", "high_fever", "headache"])
        self.assertEqual(result["predicted_disease"], "Dengue")

    def test_predict_typhoid(self):
        """Typhoid symptom cluster."""
        result = predict_disease(["chills", "vomiting", "fatigue", "high_fever", "headache", "nausea", "constipation", "abdominal_pain"])
        self.assertEqual(result["predicted_disease"], "Typhoid")

    def test_predict_chicken_pox(self):
        """Chicken pox symptom cluster."""
        result = predict_disease(["itching", "skin_rash", "fatigue", "lethargy", "high_fever", "headache"])
        self.assertEqual(result["predicted_disease"], "Chicken pox")

    def test_predict_diabetes(self):
        """Diabetes symptom cluster."""
        result = predict_disease(["fatigue", "weight_loss", "restlessness", "lethargy", "irregular_sugar_level", "blurred_and_distorted_vision", "obesity", "excessive_hunger", "increased_appetite", "polyuria"])
        self.assertIn("Diabetes", result["predicted_disease"])

    def test_predict_pneumonia(self):
        """Pneumonia symptom cluster."""
        result = predict_disease(["chills", "fatigue", "cough", "high_fever", "breathlessness", "sweating", "malaise", "phlegm", "chest_pain", "fast_heart_rate", "rusty_sputum"])
        self.assertEqual(result["predicted_disease"], "Pneumonia")

    def test_top_3_returned(self):
        """Top 3 predictions are returned."""
        result = predict_disease(["chest_pain", "breathlessness"])
        self.assertIn("top_3", result)
        self.assertGreaterEqual(len(result["top_3"]), 1)

    def test_unknown_symptoms_handled(self):
        """Unknown symptom names are gracefully ignored."""
        result = predict_disease(["xyz_unknown", "abc_fake"])
        self.assertIn("predicted_disease", result)

    def test_severity_map(self):
        """Symptom severity weights load correctly."""
        self.assertGreater(get_symptom_severity("chest_pain"), 0)
        self.assertGreater(get_symptom_severity("stomach_pain"), 0)

    def test_disease_info(self):
        """Disease info contains descriptions and precautions."""
        info = get_disease_info()
        self.assertIn("Malaria", info)
        self.assertIn("description", info["Malaria"])
        self.assertIn("precautions", info["Malaria"])
        self.assertGreater(len(info["Malaria"]["precautions"]), 0)

    def test_dataset_accuracy(self):
        """Validate model against the training dataset (spot check)."""
        BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        df = pd.read_csv(os.path.join(BASE, "dataset.csv"))
        df["Disease"] = df["Disease"].str.strip()
        symptom_cols = [c for c in df.columns if c.startswith("Symptom")]

        correct = 0
        total = 0
        # Test on a sample of rows (every 50th row)
        for idx in range(0, len(df), 50):
            row = df.iloc[idx]
            symptoms = [str(row[c]).strip() for c in symptom_cols if str(row[c]).strip() and str(row[c]).strip() != "nan"]
            if not symptoms:
                continue
            result = predict_disease(symptoms)
            if result["predicted_disease"].strip() == row["Disease"].strip():
                correct += 1
            total += 1

        accuracy = correct / total if total > 0 else 0
        print(f"\n  Dataset spot-check accuracy: {correct}/{total} = {accuracy:.2%}")
        self.assertGreater(accuracy, 0.90, f"Accuracy {accuracy:.2%} is below 90%")


class TestPhase1Input(unittest.TestCase):
    """Test input parsing and normalization."""

    def test_symptom_list_normalization(self):
        """List of symptoms is normalized correctly."""
        result = process_input({
            "age": 30, "gender": "male",
            "symptoms": ["chest_pain", "high_fever", "cough"],
        })
        self.assertIn("chest_pain", result.normalized_symptoms)
        self.assertIn("high_fever", result.normalized_symptoms)

    def test_free_text_parsing(self):
        """Free text symptoms are extracted."""
        result = process_input({
            "age": 25, "gender": "female",
            "raw_text": "I have headache and cough",
        })
        self.assertIn("headache", result.normalized_symptoms)
        self.assertIn("cough", result.normalized_symptoms)

    def test_language_detection_hindi(self):
        """Hindi text is detected."""
        lang = detect_language("mujhe bahut bukhar ho raha hai")
        self.assertEqual(lang, "hi")

    def test_language_detection_marathi(self):
        """Marathi text is detected."""
        lang = detect_language("mala khup taap aahe doka dukhtay")
        self.assertEqual(lang, "mr")

    def test_language_detection_english(self):
        """English text defaults correctly."""
        lang = detect_language("I have a headache and fever")
        self.assertEqual(lang, "en")

    def test_user_profile_created(self):
        """UserProfile is populated."""
        result = process_input({"age": 55, "gender": "male", "symptoms": ["cough"]})
        self.assertEqual(result.user_profile.age, 55)
        self.assertEqual(result.user_profile.gender, "male")

    def test_empty_symptoms(self):
        """Empty symptoms returns empty list."""
        result = process_input({"age": 20, "gender": "male", "symptoms": []})
        self.assertEqual(result.normalized_symptoms, [])


class TestNLPEngine(unittest.TestCase):
    """Test NLP symptom extraction, negation, and phrase matching."""

    def test_conversational_english(self):
        """'throwing up' → vomiting, 'stomach killing' → stomach_pain."""
        symptoms, negated = extract_symptoms_nlp(
            "I have been throwing up all day and my stomach is killing me"
        )
        self.assertIn("vomiting", symptoms)
        self.assertIn("stomach_pain", symptoms)

    def test_negation_english(self):
        """'don't have fever' excludes fever from results."""
        symptoms, negated = extract_symptoms_nlp(
            "I have a bad cough but I don't have fever"
        )
        self.assertIn("cough", symptoms)
        self.assertIn("mild_fever", negated)
        self.assertNotIn("mild_fever", symptoms)

    def test_negation_no_headache(self):
        """'no headache' excludes headache."""
        symptoms, negated = extract_symptoms_nlp(
            "I have cough and fever but no headache"
        )
        self.assertNotIn("headache", symptoms)
        self.assertIn("headache", negated)

    def test_hindi_phrases(self):
        """Hindi symptoms are correctly extracted."""
        symptoms, _ = extract_symptoms_nlp(
            "mujhe bahut tez bukhar hai aur sir mein dard hai"
        )
        self.assertIn("high_fever", symptoms)
        self.assertIn("headache", symptoms)

    def test_layman_terms(self):
        """Layman phrases map to model columns."""
        symptoms, _ = extract_symptoms_nlp(
            "my joints are hurting and I have a runny nose and keep sneezing"
        )
        self.assertIn("joint_pain", symptoms)
        self.assertIn("runny_nose", symptoms)
        self.assertIn("continuous_sneezing", symptoms)

    def test_medical_terms(self):
        """Medical terms like tachycardia, hemoptysis are recognized."""
        symptoms, _ = extract_symptoms_nlp(
            "experiencing tachycardia and hemoptysis"
        )
        self.assertIn("fast_heart_rate", symptoms)
        self.assertIn("blood_in_sputum", symptoms)

    def test_blurry_vision(self):
        """'blurry' maps to blurred_and_distorted_vision."""
        symptoms, _ = extract_symptoms_nlp("my eyes are blurry")
        self.assertIn("blurred_and_distorted_vision", symptoms)

    def test_multi_symptom_complex(self):
        """Multiple symptoms from a complex sentence are extracted."""
        symptoms, _ = extract_symptoms_nlp(
            "I feel dizzy, nauseous, losing weight and can't breathe"
        )
        self.assertIn("dizziness", symptoms)
        self.assertIn("nausea", symptoms)
        self.assertIn("weight_loss", symptoms)
        self.assertIn("breathlessness", symptoms)

    def test_empty_input(self):
        """Empty input returns empty lists."""
        symptoms, negated = extract_symptoms_nlp("")
        self.assertEqual(symptoms, [])
        self.assertEqual(negated, [])

    def test_negated_not_in_extracted(self):
        """Negated symptom never appears in extracted list."""
        symptoms, negated = extract_symptoms_nlp(
            "I have chest pain but no fever and I don't have headache"
        )
        self.assertIn("chest_pain", symptoms)
        for n in negated:
            self.assertNotIn(n, symptoms)

    def test_nlp_metadata_in_pipeline(self):
        """Pipeline response contains NLP metadata."""
        result = run_triage({
            "age": 30, "gender": "male",
            "symptoms": "I have a terrible headache and I feel nauseous",
        })
        self.assertIn("nlp", result)
        self.assertIn("extracted_symptoms", result["nlp"])
        self.assertIn("negated_symptoms", result["nlp"])
        self.assertIn("symptom_count", result["nlp"])
        self.assertGreater(result["nlp"]["symptom_count"], 0)


class TestPhase2Neglect(unittest.TestCase):
    """Test symptom neglect detection."""

    def test_neglect_detected_high_risk(self):
        """Minimization with high-risk symptoms flags neglect."""
        result = detect_neglect(
            "I have just a little chest pain",
            ["chest_pain"],
        )
        self.assertEqual(result["neglect_detected"], "Yes")
        self.assertIn("just", result["neglect_reason"].lower())

    def test_no_neglect_normal(self):
        """Normal description without minimization."""
        result = detect_neglect("I have a headache", ["headache"])
        self.assertEqual(result["neglect_detected"], "No")

    def test_contradiction_detected(self):
        """Contradiction between symptom and dismissal detected."""
        result = detect_neglect(
            "I have chest pain but it's not serious",
            ["chest_pain"],
        )
        self.assertEqual(result["neglect_detected"], "Yes")


class TestPhase3SilentEmergency(unittest.TestCase):
    """Test silent emergency detection."""

    def test_chest_pain_age_40_plus(self):
        """Chest pain in age > 40 flags as High."""
        result = detect_silent_emergency(["chest_pain"], age=55)
        self.assertEqual(result["silent_risk_flag"], "High")

    def test_chest_pain_young(self):
        """Chest pain in young person doesn't trigger age-based flag."""
        result = detect_silent_emergency(["chest_pain"], age=25)
        self.assertEqual(result["silent_risk_flag"], "Low")

    def test_fatigue_breathing_elderly(self):
        """Fatigue + breathing difficulty in elderly → High."""
        result = detect_silent_emergency(["fatigue", "breathing_difficulty"], age=60)
        self.assertEqual(result["silent_risk_flag"], "High")

    def test_no_silent_emergency(self):
        """Low-risk symptoms don't trigger silent emergency."""
        result = detect_silent_emergency(["headache", "cough"], age=25)
        self.assertEqual(result["silent_risk_flag"], "Low")


class TestPhase4Risk(unittest.TestCase):
    """Test risk classification."""

    def test_high_risk_classification(self):
        """Chest pain should classify as High."""
        result = classify_risk(["chest_pain", "breathlessness"], "No", "High")
        self.assertEqual(result["risk_level"], "High")

    def test_low_risk_classification(self):
        """Mild symptoms with no flags → Low or Medium."""
        result = classify_risk(["headache"], "No", "Low")
        self.assertIn(result["risk_level"], ["Low", "Medium"])

    def test_neglect_escalation(self):
        """Neglect detection escalates risk."""
        without = classify_risk(["headache"], "No", "Low")
        with_neglect = classify_risk(["headache"], "Yes", "Low")
        severity = {"Low": 0, "Medium": 1, "High": 2}
        self.assertGreaterEqual(
            severity[with_neglect["risk_level"]],
            severity[without["risk_level"]],
        )

    def test_ml_prediction_included(self):
        """ML prediction is included in result."""
        result = classify_risk(["chest_pain", "breathlessness", "sweating"], "No", "Low")
        self.assertIsNotNone(result["ml_prediction"])
        self.assertIn("predicted_disease", result["ml_prediction"])


class TestPhase5Explain(unittest.TestCase):
    """Test explainability narratives."""

    def test_explanation_structure(self):
        """Explanation has all 3 required sections."""
        result = generate_explanation(
            ["chest_pain"], "High", "No", "", "Low", "", None, age=50
        )
        self.assertIn("what_we_noticed", result)
        self.assertIn("why_it_matters", result)
        self.assertIn("what_this_means", result)

    def test_high_risk_explanation(self):
        """High risk gets urgent language."""
        result = generate_explanation(
            ["chest_pain"], "High", "No", "", "High",
            "Cardiac risk pattern", None, age=55
        )
        self.assertIn("medical attention", result["what_this_means"].lower())


class TestPhase6Outcome(unittest.TestCase):
    """Test outcome awareness."""

    def test_high_risk_outcome(self):
        """High risk outcome mentions delay consequences."""
        result = generate_outcome_awareness("High", ["chest_pain"])
        self.assertIn("short_term", result)
        self.assertIn("long_term", result)
        self.assertIn("delay", result["short_term"].lower())

    def test_low_risk_outcome(self):
        """Low risk outcome is reassuring."""
        result = generate_outcome_awareness("Low", ["headache"])
        self.assertIn("self-limiting", result["short_term"].lower())


class TestPhase7Action(unittest.TestCase):
    """Test actionable recommendations."""

    def test_high_risk_action(self):
        """High risk → immediate action."""
        result = generate_recommendations("High")
        self.assertIn("IMMEDIATE", result)
        self.assertIn("medical diagnosis", result.lower())

    def test_low_risk_action(self):
        """Low risk → self-care."""
        result = generate_recommendations("Low")
        self.assertIn("SELF-CARE", result)


class TestPhase8Caregiver(unittest.TestCase):
    """Test caregiver alert logic."""

    def test_high_risk_caregiver_alert(self):
        """High risk → caregiver suggestion."""
        result = evaluate_caregiver_alert("High", age=60)
        self.assertEqual(result["caregiver_alert_suggestion"], "Yes")

    def test_low_risk_no_alert(self):
        """Low risk → no caregiver alert."""
        result = evaluate_caregiver_alert("Low", age=25)
        self.assertEqual(result["caregiver_alert_suggestion"], "No")


class TestPhase9Language(unittest.TestCase):
    """Test multilingual response."""

    def test_hindi_localization(self):
        """Hindi localization translates risk level."""
        response = {"risk_level": "High", "neglect_detected": "Yes"}
        result = localize_response(response, "hi")
        self.assertEqual(result["risk_level"], "उच्च")
        self.assertEqual(result["neglect_detected"], "हाँ")

    def test_marathi_localization(self):
        """Marathi localization translates risk level."""
        response = {"risk_level": "Medium", "neglect_detected": "No"}
        result = localize_response(response, "mr")
        self.assertEqual(result["risk_level"], "मध्यम")
        self.assertEqual(result["neglect_detected"], "नाही")

    def test_english_passthrough(self):
        """English response is unchanged."""
        response = {"risk_level": "High"}
        result = localize_response(response, "en")
        self.assertEqual(result["risk_level"], "High")


class TestPipeline(unittest.TestCase):
    """Test the full triage pipeline."""

    def test_full_high_risk_pipeline(self):
        """Full pipeline for a high-risk scenario."""
        result = run_triage({
            "age": 55, "gender": "male",
            "symptoms": ["chest_pain", "breathlessness", "sweating"],
            "raw_text": "I have just a little chest pain",
            "language": "en",
        })
        self.assertEqual(result["risk_level"], "High")
        self.assertEqual(result["neglect_detected"], "Yes")
        self.assertIn("disclaimer", result)
        self.assertIn("explanation", result)
        self.assertIn("what_if_ignored", result)
        self.assertIn("recommended_action", result)

    def test_full_low_risk_pipeline(self):
        """Full pipeline for a low-risk scenario."""
        result = run_triage({
            "age": 22, "gender": "female",
            "symptoms": ["headache", "cough"],
            "language": "en",
        })
        self.assertIn(result["risk_level"], ["Low", "Medium"])

    def test_empty_symptoms_handled(self):
        """Empty symptoms returns graceful response."""
        result = run_triage({"age": 30, "symptoms": []})
        self.assertEqual(result["risk_level"], "Low")

    def test_hindi_pipeline(self):
        """Hindi response returns translated fields."""
        result = run_triage({
            "age": 45, "symptoms": ["chest_pain"],
            "language": "hi",
        })
        self.assertIn(result["risk_level"], ["उच्च", "मध्यम", "कम"])


class TestAPIEndpoints(unittest.TestCase):
    """Test Flask API endpoints."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_health_check(self):
        """GET / returns status."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "Avalon backend running")

    def test_triage_endpoint(self):
        """POST /triage returns valid response."""
        response = self.client.post("/triage", json={
            "age": 40, "gender": "male",
            "symptoms": ["high_fever", "cough", "headache"],
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("risk_level", data)
        self.assertIn("explanation", data)
        self.assertIn("recommended_action", data)

    def test_triage_no_data(self):
        """POST /triage with empty body returns error."""
        response = self.client.post("/triage", json={})
        self.assertEqual(response.status_code, 400)

    def test_symptoms_endpoint(self):
        """GET /symptoms returns symptom list."""
        response = self.client.get("/symptoms")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total"], 131)
        self.assertIn("categorized", data)

    def test_diseases_endpoint(self):
        """GET /diseases returns disease list."""
        response = self.client.get("/diseases")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(data["total"], 30)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  HEALTH TRIAGE COPILOT – TEST SUITE")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
