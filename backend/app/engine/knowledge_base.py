"""
Symptom knowledge base used across all triage phases.
Maps layman terms → medical concepts, defines risk clusters,
minimization keywords, and silent-emergency patterns.
"""

# ── Layman → Normalized Symptom Mapping ──────────────────────────────────────
SYMPTOM_SYNONYMS: dict[str, str] = {
    # Chest / cardiac
    "chest pain": "chest_pain",
    "chest tightness": "chest_pain",
    "chest pressure": "chest_pain",
    "heart hurts": "chest_pain",
    "heavy feeling in chest": "chest_pain",
    # Breathing
    "shortness of breath": "breathing_difficulty",
    "breathing difficulty": "breathing_difficulty",
    "can't breathe": "breathing_difficulty",
    "breathless": "breathing_difficulty",
    "difficulty breathing": "breathing_difficulty",
    "gasping": "breathing_difficulty",
    "saans nahi aa rahi": "breathing_difficulty",            # Hindi
    "shwas ghene kathin": "breathing_difficulty",            # Marathi
    # Head
    "headache": "headache",
    "head pain": "headache",
    "migraine": "headache",
    "sir dard": "headache",                                  # Hindi
    "doka dukhtay": "headache",                              # Marathi
    # Fever
    "fever": "fever",
    "high temperature": "fever",
    "feeling hot": "fever",
    "bukhar": "fever",                                       # Hindi
    "taap": "fever",                                         # Marathi
    # Cough
    "cough": "cough",
    "khansi": "cough",                                       # Hindi
    "khokalaa": "cough",                                     # Marathi
    # Fatigue
    "fatigue": "fatigue",
    "tiredness": "fatigue",
    "exhaustion": "fatigue",
    "feeling weak": "fatigue",
    "thakaan": "fatigue",                                    # Hindi
    # Nausea / vomiting
    "nausea": "nausea",
    "vomiting": "vomiting",
    "throwing up": "vomiting",
    "ulti": "vomiting",                                      # Hindi
    # Pain – abdomen
    "stomach pain": "abdominal_pain",
    "abdominal pain": "abdominal_pain",
    "belly pain": "abdominal_pain",
    "pet dard": "abdominal_pain",                            # Hindi
    "potaat dukhte": "abdominal_pain",                       # Marathi
    # Dizziness
    "dizziness": "dizziness",
    "feeling dizzy": "dizziness",
    "lightheaded": "dizziness",
    "chakkar": "dizziness",                                  # Hindi
    # Numbness
    "numbness": "numbness",
    "tingling": "numbness",
    "pins and needles": "numbness",
    # Vision
    "blurred vision": "vision_change",
    "vision change": "vision_change",
    "can't see properly": "vision_change",
    # Speech
    "slurred speech": "speech_difficulty",
    "difficulty speaking": "speech_difficulty",
    "can't talk properly": "speech_difficulty",
    # Swelling
    "swelling": "swelling",
    "swollen legs": "leg_swelling",
    "swollen feet": "leg_swelling",
    # Skin
    "rash": "rash",
    "skin rash": "rash",
    # Sore throat
    "sore throat": "sore_throat",
    "throat pain": "sore_throat",
    "gala dard": "sore_throat",                              # Hindi
    # Body ache
    "body ache": "body_ache",
    "body pain": "body_ache",
    "muscle pain": "body_ache",
    "badan dard": "body_ache",                               # Hindi
    # Palpitations
    "palpitations": "palpitations",
    "heart racing": "palpitations",
    "heart beating fast": "palpitations",
    # Confusion
    "confusion": "confusion",
    "feeling confused": "confusion",
    "disoriented": "confusion",
    # Fainting
    "fainting": "fainting",
    "passed out": "fainting",
    "lost consciousness": "fainting",
    # Cold / flu
    "cold": "cold",
    "runny nose": "cold",
    "sneezing": "cold",
    "sardi": "cold",                                         # Hindi
}

# ── High-Risk Symptom Clusters ───────────────────────────────────────────────
# Each entry: (frozenset of normalized symptoms, severity label, note)
HIGH_RISK_CLUSTERS: list[tuple[frozenset[str], str, str]] = [
    (
        frozenset({"chest_pain", "breathing_difficulty"}),
        "High",
        "Combination of chest pain and breathing difficulty can sometimes be associated with serious cardiac or pulmonary conditions.",
    ),
    (
        frozenset({"chest_pain", "numbness"}),
        "High",
        "Chest pain with numbness can sometimes be associated with serious cardiac events.",
    ),
    (
        frozenset({"headache", "vision_change", "numbness"}),
        "High",
        "Sudden severe headache with vision changes and numbness can sometimes be associated with serious neurological conditions.",
    ),
    (
        frozenset({"headache", "speech_difficulty"}),
        "High",
        "Headache with speech difficulty can sometimes be associated with serious neurological conditions.",
    ),
    (
        frozenset({"numbness", "speech_difficulty"}),
        "High",
        "Numbness with speech difficulty can sometimes point to urgent neurological events.",
    ),
    (
        frozenset({"fever", "breathing_difficulty", "confusion"}),
        "High",
        "Fever with breathing difficulty and confusion can sometimes indicate a severe systemic infection.",
    ),
    (
        frozenset({"abdominal_pain", "vomiting", "fever"}),
        "Medium",
        "Abdominal pain with vomiting and fever may need professional evaluation.",
    ),
    (
        frozenset({"fever", "cough", "breathing_difficulty"}),
        "High",
        "Fever, cough, and breathing difficulty together can sometimes be associated with serious respiratory infections.",
    ),
    (
        frozenset({"dizziness", "fainting"}),
        "High",
        "Dizziness with fainting episodes warrants prompt medical attention.",
    ),
    (
        frozenset({"chest_pain", "palpitations"}),
        "High",
        "Chest pain with palpitations can sometimes be associated with cardiac arrhythmias.",
    ),
    (
        frozenset({"fever", "rash"}),
        "Medium",
        "Fever with rash can indicate infections that may need medical evaluation.",
    ),
]

# ── Individual High-Severity Symptoms ────────────────────────────────────────
ALWAYS_HIGH_SYMPTOMS: set[str] = {
    "chest_pain",
    "breathing_difficulty",
    "speech_difficulty",
    "fainting",
    "confusion",
}

MEDIUM_SYMPTOMS: set[str] = {
    "fever",
    "vomiting",
    "abdominal_pain",
    "palpitations",
    "vision_change",
    "numbness",
    "dizziness",
    "leg_swelling",
}

LOW_SYMPTOMS: set[str] = {
    "headache",
    "cough",
    "cold",
    "sore_throat",
    "body_ache",
    "fatigue",
    "rash",
    "nausea",
}

# ── Minimization / Neglect Phrases ───────────────────────────────────────────
MINIMIZATION_PHRASES: list[str] = [
    "just",
    "only",
    "a little",
    "not serious",
    "nothing much",
    "it's fine",
    "it will go away",
    "no big deal",
    "small pain",
    "minor",
    "slight",
    "thoda sa",           # Hindi – "a little"
    "kuch nahi",          # Hindi – "nothing"
    "bas thoda",          # Hindi – "just a little"
    "kaahi nahi",         # Marathi – "nothing"
]

# ── Silent Emergency Patterns ────────────────────────────────────────────────
# (symptom set, age_modifier, gender_modifier, explanation)
SILENT_EMERGENCY_PATTERNS: list[dict] = [
    {
        "symptoms": {"chest_pain"},
        "age_min": 40,
        "gender": None,
        "flag": "High",
        "explanation": "Chest pain in individuals above 40 can sometimes be associated with serious cardiac conditions, even when it feels mild.",
    },
    {
        "symptoms": {"fatigue", "breathing_difficulty"},
        "age_min": 50,
        "gender": None,
        "flag": "High",
        "explanation": "Persistent fatigue with breathing difficulty in individuals above 50 may sometimes be linked to cardiac or pulmonary conditions.",
    },
    {
        "symptoms": {"numbness"},
        "age_min": 30,
        "gender": None,
        "flag": "Moderate",
        "explanation": "Sudden onset numbness can sometimes be associated with neurological conditions that benefit from early evaluation.",
    },
    {
        "symptoms": {"headache", "vision_change"},
        "age_min": None,
        "gender": None,
        "flag": "High",
        "explanation": "Severe headache with vision changes can sometimes be associated with serious neurological conditions.",
    },
    {
        "symptoms": {"dizziness", "palpitations"},
        "age_min": None,
        "gender": None,
        "flag": "Moderate",
        "explanation": "Dizziness with palpitations may indicate cardiac rhythm issues that benefit from medical evaluation.",
    },
    {
        "symptoms": {"abdominal_pain"},
        "age_min": 60,
        "gender": None,
        "flag": "Moderate",
        "explanation": "Abdominal pain in individuals over 60 can sometimes mask serious underlying conditions.",
    },
]

# ── Language Detection Hints ─────────────────────────────────────────────────
HINDI_MARKERS = [
    "hai", "mujhe", "mera", "dard", "ho raha", "bukhar",
    "pet", "sir", "bahut", "thoda", "kuch", "nahi",
    "saans", "gala", "badan", "tang", "pareshani",
]

MARATHI_MARKERS = [
    "aahe", "mala", "mazha", "dukhtay", "hotay", "taap",
    "potaat", "doka", "khup", "thoda", "kaahi", "nahi",
    "shwas", "ghasa", "anga", "tras",
]
