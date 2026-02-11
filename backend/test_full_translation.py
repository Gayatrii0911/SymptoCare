#!/usr/bin/env python
"""
Test full translation with precautions and caregiver messages
"""

from app.engine.translations import translate_full_text

# Test precaution translation
precautions_text = """
SPECIFIC PRECAUTIONS:
• Avoid fatty spicy food
• Wash hands through
• Medication
• Consult doctor
"""

print("=" * 60)
print("PRECAUTIONS TRANSLATION TEST")
print("=" * 60)

print("\n📝 ENGLISH TEXT:")
print(precautions_text)

print("\n🇮🇳 HINDI TRANSLATION:")
hindi_result = translate_full_text(precautions_text, "hi")
print(hindi_result)

print("\n🇲🇷 MARATHI TRANSLATION:")
marathi_result = translate_full_text(precautions_text, "mr")
print(marathi_result)

# Test caregiver message
caregiver_msg = (
    "Given the urgency of your symptoms, we strongly recommend "
    "informing a trusted family member, friend, or caregiver. "
    "Having someone aware of your situation can help ensure you "
    "receive timely assistance, especially if symptoms worsen."
)

print("\n" + "=" * 60)
print("CAREGIVER MESSAGE TRANSLATION TEST")
print("=" * 60)

print("\n📝 ENGLISH TEXT:")
print(caregiver_msg)

print("\n🇮🇳 HINDI TRANSLATION:")
hindi_caregiver = translate_full_text(caregiver_msg, "hi")
print(hindi_caregiver)

print("\n🇲🇷 MARATHI TRANSLATION:")
marathi_caregiver = translate_full_text(caregiver_msg, "mr")
print(marathi_caregiver)

# Test mixed text
mixed = "IMMEDIATE ACTION RECOMMENDED: Please seek medical attention as soon as possible. Visit the nearest hospital or call emergency services. Do not drive yourself — ask someone to take you or call an ambulance."

print("\n" + "=" * 60)
print("MIXED ACTION TEXT TRANSLATION TEST")
print("=" * 60)

print("\n📝 ENGLISH TEXT:")
print(mixed)

print("\n🇮🇳 HINDI TRANSLATION:")
hindi_mixed = translate_full_text(mixed, "hi")
print(hindi_mixed)

print("\n🇲🇷 MARATHI TRANSLATION:")
marathi_mixed = translate_full_text(mixed, "mr")
print(marathi_mixed)

print("\n" + "=" * 60)
print("✅ TRANSLATION TEST COMPLETE")
print("=" * 60)
