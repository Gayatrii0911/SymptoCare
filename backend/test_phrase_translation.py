#!/usr/bin/env python3
"""
Test script to verify comprehensive text translation with medical phrases.
"""

import sys
sys.path.insert(0, '.')

from app.engine.translations import translate_full_text, MEDICAL_PHRASES

def test_phrase_translation():
    """Test that full sentences are being translated."""
    print("=" * 70)
    print("Testing Full Text Translation (Phrases + Symptoms)")
    print("=" * 70)
    
    test_text = 'You reported the following symptoms: fatigue, headache. Your age is 45. Please seek medical attention as soon as possible. IMMEDIATE ACTION RECOMMENDED.'
    
    print("\n📝 Original English Text:")
    print(f"  {test_text}")
    
    print("\n🇮🇳 Hindi Translation:")
    hi_text = translate_full_text(test_text, "hi")
    print(f"  {hi_text}")
    
    print("\n🇮🇳 Marathi Translation:")
    mr_text = translate_full_text(test_text, "mr")
    print(f"  {mr_text}")
    
    print("\n📊 Translation Coverage Statistics:")
    print(f"  Hindi phrases: {len(MEDICAL_PHRASES.get('hi', {}))} phrases found")
    print(f"  Marathi phrases: {len(MEDICAL_PHRASES.get('mr', {}))} phrases found")
    
    # Verify translations are different from English
    assert hi_text != test_text, "Hindi text should be translated"
    assert mr_text != test_text, "Marathi text should be translated"
    assert "सिरदर्द" in hi_text or "डोकेदुखी" in mr_text, "Symptoms should be translated"
    
    print("\n✅ Full text translation verified!")


if __name__ == "__main__":
    try:
        test_phrase_translation()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
