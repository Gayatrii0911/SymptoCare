#!/usr/bin/env python
"""
Test to check if disease descriptions are being translated
"""

from app.engine.pipeline import run_triage

# Test case: Hypoglycemia symptoms
test_data = {
    "age": 35,
    "gender": "male",
    "symptoms": ["high_fever", "sweating", "dizziness"],  # Hypoglycemia-like
    "language": "mr"  # Marathi
}

result = run_triage(test_data)

print("=" * 80)
print("DISEASE DESCRIPTION TRANSLATION TEST")
print("=" * 80)

print("\n🏥 Predicted Condition:", result.get("predicted_condition"))
print("\n📝 Why It Matters (First 200 chars):")
why_it_matters = result.get("explanation", {}).get("why_it_matters", "")
print(why_it_matters[:200] if why_it_matters else "N/A")

print("\n🔍 Full 'Why It Matters' Text:")
print(why_it_matters)

print("\n" + "=" * 80)
print("Checking for English text (disease description)...")
if "Hypoglycemia" in why_it_matters or "blood sugar" in why_it_matters:
    print("❌ FOUND ENGLISH TEXT - Disease description not translated!")
else:
    print("✅ No English disease description found")
print("=" * 80)
