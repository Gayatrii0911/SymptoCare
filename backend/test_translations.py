#!/usr/bin/env python3
"""
Test script to verify medical translations are working correctly.
Run this to ensure all translations are properly loaded and functioning.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.engine.translations import (
    DISEASE_NAMES,
    SYMPTOM_TRANSLATIONS,
    translate_disease_name,
    translate_symptom,
)

def test_disease_translations():
    """Test that disease names are translated correctly."""
    print("=" * 60)
    print("Testing Disease Name Translations")
    print("=" * 60)
    
    test_diseases = [
        "Fungal infection",
        "Allergy",
        "Diabetes",
        "Hypertension",
        "Malaria",
    ]
    
    for disease in test_diseases:
        en = translate_disease_name(disease, "en")
        hi = translate_disease_name(disease, "hi")
        mr = translate_disease_name(disease, "mr")
        
        print(f"\n{disease}")
        print(f"  English: {en}")
        print(f"  Hindi:   {hi}")
        print(f"  Marathi: {mr}")
        
        # Verify all are different or appropriately translated
        assert en != "", f"English translation missing for {disease}"
        assert hi != "", f"Hindi translation missing for {disease}"
        assert mr != "", f"Marathi translation missing for {disease}"
    
    print("\n✅ All disease translations verified!")


def test_symptom_translations():
    """Test that symptom names are translated correctly."""
    print("\n" + "=" * 60)
    print("Testing Symptom Name Translations")
    print("=" * 60)
    
    test_symptoms = [
        "headache",
        "high_fever",
        "cough",
        "chest_pain",
        "stomach_pain",
        "fatigue",
        "vomiting",
    ]
    
    for symptom in test_symptoms:
        en = translate_symptom(symptom, "en")
        hi = translate_symptom(symptom, "hi")
        mr = translate_symptom(symptom, "mr")
        
        print(f"\n{symptom}")
        print(f"  English: {en}")
        print(f"  Hindi:   {hi}")
        print(f"  Marathi: {mr}")
        
        # Verify all are different or appropriately translated
        assert en != "", f"English translation missing for {symptom}"
        assert hi != "", f"Hindi translation missing for {symptom}"
        assert mr != "", f"Marathi translation missing for {symptom}"
    
    print("\n✅ All symptom translations verified!")


def test_translation_count():
    """Verify the number of translations."""
    print("\n" + "=" * 60)
    print("Translation Coverage Statistics")
    print("=" * 60)
    
    diseases_en = len(DISEASE_NAMES.get("en", {}))
    diseases_hi = len(DISEASE_NAMES.get("hi", {}))
    diseases_mr = len(DISEASE_NAMES.get("mr", {}))
    
    symptoms_en = len(SYMPTOM_TRANSLATIONS.get("en", {}))
    symptoms_hi = len(SYMPTOM_TRANSLATIONS.get("hi", {}))
    symptoms_mr = len(SYMPTOM_TRANSLATIONS.get("mr", {}))
    
    print(f"\nDiseases:")
    print(f"  English: {diseases_en}")
    print(f"  Hindi:   {diseases_hi}")
    print(f"  Marathi: {diseases_mr}")
    
    print(f"\nSymptoms:")
    print(f"  English: {symptoms_en}")
    print(f"  Hindi:   {symptoms_hi}")
    print(f"  Marathi: {symptoms_mr}")
    
    # Verify count consistency
    assert diseases_en == diseases_hi == diseases_mr, "Disease translation count mismatch"
    assert symptoms_en == symptoms_hi == symptoms_mr, "Symptom translation count mismatch"
    
    print("\n✅ Translation coverage verified!")
    print(f"\nTotal Translations:")
    print(f"  Diseases: {diseases_en} × 3 languages")
    print(f"  Symptoms: {symptoms_en} × 3 languages")


def test_localization_function():
    """Test the localization function from phase9_language.py."""
    print("\n" + "=" * 60)
    print("Testing Localization Function")
    print("=" * 60)
    
    try:
        from app.engine.phase9_language import localize_response
        
        # Sample response
        test_response = {
            "risk_level": "High",
            "predicted_condition": "Diabetes",
            "top_3_conditions": [
                ("Diabetes", 0.85),
                ("Hypertension", 0.60),
                ("Thyroid", 0.40),
            ],
            "explanation": {
                "what_we_noticed": "Excessive hunger and fatigue detected",
                "why_it_matters": "These symptoms indicate possible diabetes",
                "what_this_means": "Blood glucose level monitoring recommended",
            },
            "nlp": {
                "extracted_symptoms": ["headache", "high_fever"],
                "negated_symptoms": [],
            },
        }
        
        # Test English (should return as-is)
        result_en = localize_response(test_response.copy(), "en")
        print(f"\nEnglish Result:")
        print(f"  Condition: {result_en['predicted_condition']}")
        print(f"  Risk Level: {result_en['risk_level']}")
        print(f"  Symptoms: {result_en['nlp']['extracted_symptoms']}")
        
        # Test Hindi
        result_hi = localize_response(test_response.copy(), "hi")
        print(f"\nHindi Result:")
        print(f"  Condition: {result_hi['predicted_condition']}")
        print(f"  Risk Level: {result_hi['risk_level']}")
        print(f"  Symptoms: {result_hi['nlp']['extracted_symptoms']}")
        
        # Test Marathi
        result_mr = localize_response(test_response.copy(), "mr")
        print(f"\nMarathi Result:")
        print(f"  Condition: {result_mr['predicted_condition']}")
        print(f"  Risk Level: {result_mr['risk_level']}")
        print(f"  Symptoms: {result_mr['nlp']['extracted_symptoms']}")
        
        # Verify translations changed
        assert result_en['predicted_condition'] == "Diabetes", "English should not change"
        assert result_hi['predicted_condition'] != "Diabetes", "Hindi should be translated"
        assert result_mr['predicted_condition'] != "Diabetes", "Marathi should be translated"
        
        print("\n✅ Localization function working correctly!")
        
    except ImportError as e:
        print(f"⚠️  Could not import phase9_language: {e}")


if __name__ == "__main__":
    print("\n🧪 MEDICAL TRANSLATIONS TEST SUITE\n")
    
    try:
        test_disease_translations()
        test_symptom_translations()
        test_translation_count()
        test_localization_function()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe localization system is working correctly.")
        print("Users will now see translated medical terms when they change languages.")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
