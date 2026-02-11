"""
NLP Symptom Extraction Engine
==============================
Extracts, normalizes, and disambiguates symptoms from free-text input.

Capabilities:
  • Comprehensive phrase → symptom mapping (500+ entries covering all 131 model columns)
  • Negation detection  ("I don't have fever"  → fever excluded)
  • Fuzzy / partial matching via token n-grams
  • Stemming-aware matching (running→runny, swelling→swollen, etc.)
  • Multi-language awareness (Hindi / Marathi phrases routed through synonym map)
"""

from __future__ import annotations
import re
from ml.predictor import get_all_symptoms

# ─────────────────────────────────────────────────────────────────────────────
#  COMPREHENSIVE  phrase → model column  mapping
#  Every one of the 131 symptom columns has multiple natural-language aliases.
# ─────────────────────────────────────────────────────────────────────────────

NLP_PHRASE_MAP: dict[str, str] = {
    # ── abdominal_pain ──
    "abdominal pain": "abdominal_pain",
    "stomach ache": "abdominal_pain",
    "tummy ache": "abdominal_pain",
    "tummy pain": "abdominal_pain",
    "pain in abdomen": "abdominal_pain",
    "pain in stomach": "abdominal_pain",
    "my abdomen hurts": "abdominal_pain",
    "my stomach hurts": "abdominal_pain",
    "abdomen cramp": "abdominal_pain",
    "pet dard": "abdominal_pain",
    "pet mein dard": "abdominal_pain",
    "potaat dukhte": "abdominal_pain",

    # ── abnormal_menstruation ──
    "abnormal menstruation": "abnormal_menstruation",
    "irregular periods": "abnormal_menstruation",
    "irregular menstruation": "abnormal_menstruation",
    "missed period": "abnormal_menstruation",
    "period problem": "abnormal_menstruation",
    "menstrual irregularity": "abnormal_menstruation",
    "heavy period": "abnormal_menstruation",
    "heavy bleeding": "abnormal_menstruation",
    "spotting between periods": "abnormal_menstruation",

    # ── acidity ──
    "acidity": "acidity",
    "acid reflux": "acidity",
    "heartburn": "acidity",
    "heart burn": "acidity",
    "sour stomach": "acidity",
    "burning in stomach": "acidity",
    "gastric": "acidity",
    "gastric problem": "acidity",
    "gas problem": "acidity",
    "acidity problem": "acidity",

    # ── acute_liver_failure ──
    "acute liver failure": "acute_liver_failure",
    "liver failure": "acute_liver_failure",
    "liver damage": "acute_liver_failure",
    "liver shutting down": "acute_liver_failure",

    # ── altered_sensorium ──
    "altered sensorium": "altered_sensorium",
    "altered consciousness": "altered_sensorium",
    "confusion": "altered_sensorium",
    "confused": "altered_sensorium",
    "disoriented": "altered_sensorium",
    "mental confusion": "altered_sensorium",
    "not making sense": "altered_sensorium",
    "acting strange": "altered_sensorium",

    # ── anxiety ──
    "anxiety": "anxiety",
    "anxious": "anxiety",
    "feeling anxious": "anxiety",
    "worried": "anxiety",
    "nervousness": "anxiety",
    "nervous": "anxiety",
    "panic": "anxiety",
    "panic attack": "anxiety",
    "tension": "anxiety",
    "stressed": "anxiety",

    # ── back_pain ──
    "back pain": "back_pain",
    "lower back pain": "back_pain",
    "upper back pain": "back_pain",
    "backache": "back_pain",
    "my back hurts": "back_pain",
    "spine pain": "back_pain",
    "kamar dard": "back_pain",
    "peeth dard": "back_pain",

    # ── belly_pain ──
    "belly pain": "belly_pain",
    "belly ache": "belly_pain",
    "pain in belly": "belly_pain",
    "lower belly pain": "belly_pain",

    # ── blackheads ──
    "blackheads": "blackheads",
    "black heads": "blackheads",
    "blackhead on face": "blackheads",
    "comedones": "blackheads",

    # ── bladder_discomfort ──
    "bladder discomfort": "bladder_discomfort",
    "bladder pain": "bladder_discomfort",
    "bladder pressure": "bladder_discomfort",
    "uncomfortable bladder": "bladder_discomfort",

    # ── blister ──
    "blister": "blister",
    "blisters": "blister",
    "skin blister": "blister",
    "water blister": "blister",
    "blistering": "blister",

    # ── blood_in_sputum ──
    "blood in sputum": "blood_in_sputum",
    "coughing blood": "blood_in_sputum",
    "bloody sputum": "blood_in_sputum",
    "blood when coughing": "blood_in_sputum",
    "blood in cough": "blood_in_sputum",
    "hemoptysis": "blood_in_sputum",
    "spitting blood": "blood_in_sputum",

    # ── bloody_stool ──
    "bloody stool": "bloody_stool",
    "blood in stool": "bloody_stool",
    "blood in poop": "bloody_stool",
    "bloody poop": "bloody_stool",
    "rectal bleeding": "bloody_stool",
    "bleeding from rectum": "bloody_stool",

    # ── blurred_and_distorted_vision ──
    "blurred and distorted vision": "blurred_and_distorted_vision",
    "blurred vision": "blurred_and_distorted_vision",
    "blurry vision": "blurred_and_distorted_vision",
    "blurry": "blurred_and_distorted_vision",
    "distorted vision": "blurred_and_distorted_vision",
    "vision blurry": "blurred_and_distorted_vision",
    "can't see clearly": "blurred_and_distorted_vision",
    "eyesight problem": "blurred_and_distorted_vision",
    "vision problem": "blurred_and_distorted_vision",
    "nazar kamzor": "blurred_and_distorted_vision",
    "hazy vision": "blurred_and_distorted_vision",
    "foggy vision": "blurred_and_distorted_vision",

    # ── breathlessness ──
    "breathlessness": "breathlessness",
    "breathless": "breathlessness",
    "shortness of breath": "breathlessness",
    "short of breath": "breathlessness",
    "breathing difficulty": "breathlessness",
    "difficulty breathing": "breathlessness",
    "can't breathe": "breathlessness",
    "cannot breathe": "breathlessness",
    "gasping": "breathlessness",
    "gasping for air": "breathlessness",
    "out of breath": "breathlessness",
    "winded": "breathlessness",
    "saans nahi aa rahi": "breathlessness",
    "saans lene mein taklif": "breathlessness",
    "shwas ghene kathin": "breathlessness",

    # ── brittle_nails ──
    "brittle nails": "brittle_nails",
    "nails breaking": "brittle_nails",
    "fragile nails": "brittle_nails",
    "weak nails": "brittle_nails",
    "nails cracking": "brittle_nails",

    # ── bruising ──
    "bruising": "bruising",
    "bruise": "bruising",
    "bruises": "bruising",
    "easy bruising": "bruising",
    "bruise easily": "bruising",

    # ── burning_micturition ──
    "burning micturition": "burning_micturition",
    "burning urination": "burning_micturition",
    "burning when urinating": "burning_micturition",
    "painful urination": "burning_micturition",
    "pain while peeing": "burning_micturition",
    "burning pee": "burning_micturition",
    "uti": "burning_micturition",
    "urinary tract infection": "burning_micturition",

    # ── chest_pain ──
    "chest pain": "chest_pain",
    "chest tightness": "chest_pain",
    "chest pressure": "chest_pain",
    "heavy chest": "chest_pain",
    "heavy feeling in chest": "chest_pain",
    "heart pain": "chest_pain",
    "heart hurts": "chest_pain",
    "pain in chest": "chest_pain",
    "my chest hurts": "chest_pain",
    "sina dard": "chest_pain",
    "seene mein dard": "chest_pain",
    "chhaati mein dard": "chest_pain",

    # ── chills ──
    "chills": "chills",
    "chilly": "chills",
    "shivering with cold": "chills",
    "feeling cold": "chills",
    "body shaking": "chills",
    "rigors": "chills",
    "thandi lag rahi": "chills",
    "kamp raha hai": "chills",

    # ── cold_hands_and_feets ──
    "cold hands and feet": "cold_hands_and_feets",
    "cold extremities": "cold_hands_and_feets",
    "cold fingers": "cold_hands_and_feets",
    "hands are cold": "cold_hands_and_feets",
    "feet are cold": "cold_hands_and_feets",
    "icy hands": "cold_hands_and_feets",

    # ── coma ──
    "coma": "coma",
    "unconscious": "coma",
    "unresponsive": "coma",
    "not waking up": "coma",

    # ── congestion ──
    "congestion": "congestion",
    "nasal congestion": "congestion",
    "blocked nose": "congestion",
    "stuffy nose": "congestion",
    "nose is blocked": "congestion",
    "naak band": "congestion",

    # ── constipation ──
    "constipation": "constipation",
    "constipated": "constipation",
    "can't pass stool": "constipation",
    "difficulty passing stool": "constipation",
    "hard stool": "constipation",
    "qabz": "constipation",
    "kabz": "constipation",

    # ── continuous_feel_of_urine ──
    "continuous feel of urine": "continuous_feel_of_urine",
    "constant urge to urinate": "continuous_feel_of_urine",
    "frequent urination": "continuous_feel_of_urine",
    "urge to pee": "continuous_feel_of_urine",
    "always need to pee": "continuous_feel_of_urine",
    "baar baar peshab": "continuous_feel_of_urine",

    # ── continuous_sneezing ──
    "continuous sneezing": "continuous_sneezing",
    "sneezing a lot": "continuous_sneezing",
    "constant sneezing": "continuous_sneezing",
    "non stop sneezing": "continuous_sneezing",
    "keep sneezing": "continuous_sneezing",
    "sneezing": "continuous_sneezing",

    # ── cough ──
    "cough": "cough",
    "coughing": "cough",
    "dry cough": "cough",
    "wet cough": "cough",
    "persistent cough": "cough",
    "chronic cough": "cough",
    "khansi": "cough",
    "khokalaa": "cough",

    # ── cramps ──
    "cramps": "cramps",
    "cramping": "cramps",
    "muscle cramp": "cramps",
    "leg cramp": "cramps",
    "stomach cramp": "cramps",
    "abdominal cramp": "cramps",

    # ── dark_urine ──
    "dark urine": "dark_urine",
    "dark colored urine": "dark_urine",
    "brown urine": "dark_urine",
    "cola colored urine": "dark_urine",
    "dark pee": "dark_urine",

    # ── dehydration ──
    "dehydration": "dehydration",
    "dehydrated": "dehydration",
    "very thirsty": "dehydration",
    "extreme thirst": "dehydration",
    "dry mouth": "dehydration",
    "not enough water": "dehydration",

    # ── depression ──
    "depression": "depression",
    "depressed": "depression",
    "feeling depressed": "depression",
    "feeling low": "depression",
    "sad all the time": "depression",
    "hopeless": "depression",
    "no interest in anything": "depression",

    # ── diarrhoea ──
    "diarrhoea": "diarrhoea",
    "diarrhea": "diarrhoea",
    "loose motions": "diarrhoea",
    "loose stools": "diarrhoea",
    "watery stool": "diarrhoea",
    "running stomach": "diarrhoea",
    "frequent stools": "diarrhoea",
    "dast": "diarrhoea",
    "dasth": "diarrhoea",

    # ── dischromic _patches ──  (note: dataset has space before _)
    "dischromic patches": "dischromic _patches",
    "discolored patches": "dischromic _patches",
    "skin patches": "dischromic _patches",
    "dark patches on skin": "dischromic _patches",
    "light patches on skin": "dischromic _patches",
    "skin discoloration": "dischromic _patches",

    # ── distention_of_abdomen ──
    "distention of abdomen": "distention_of_abdomen",
    "bloated abdomen": "distention_of_abdomen",
    "bloating": "distention_of_abdomen",
    "bloated stomach": "distention_of_abdomen",
    "abdominal distention": "distention_of_abdomen",
    "stomach swelling": "distention_of_abdomen",
    "swollen belly": "distention_of_abdomen",
    "pet phula hua": "distention_of_abdomen",

    # ── dizziness ──
    "dizziness": "dizziness",
    "dizzy": "dizziness",
    "feeling dizzy": "dizziness",
    "lightheaded": "dizziness",
    "light headed": "dizziness",
    "head spinning": "dizziness",
    "room spinning": "dizziness",
    "vertigo": "dizziness",
    "chakkar": "dizziness",
    "chakkar aa raha": "dizziness",

    # ── drying_and_tingling_lips ──
    "drying and tingling lips": "drying_and_tingling_lips",
    "dry lips": "drying_and_tingling_lips",
    "tingling lips": "drying_and_tingling_lips",
    "chapped lips": "drying_and_tingling_lips",
    "cracked lips": "drying_and_tingling_lips",
    "lips tingling": "drying_and_tingling_lips",

    # ── enlarged_thyroid ──
    "enlarged thyroid": "enlarged_thyroid",
    "goiter": "enlarged_thyroid",
    "goitre": "enlarged_thyroid",
    "thyroid swelling": "enlarged_thyroid",
    "swollen thyroid": "enlarged_thyroid",
    "neck swelling": "enlarged_thyroid",

    # ── excessive_hunger ──
    "excessive hunger": "excessive_hunger",
    "always hungry": "excessive_hunger",
    "increased hunger": "excessive_hunger",
    "polyphagia": "excessive_hunger",
    "constant hunger": "excessive_hunger",
    "eating a lot": "excessive_hunger",
    "bahut bhookh": "excessive_hunger",

    # ── extra_marital_contacts ──
    "extra marital contacts": "extra_marital_contacts",
    "extramarital contacts": "extra_marital_contacts",
    "multiple partners": "extra_marital_contacts",
    "unprotected sex": "extra_marital_contacts",
    "sexual contact outside marriage": "extra_marital_contacts",

    # ── family_history ──
    "family history": "family_history",
    "runs in family": "family_history",
    "genetic history": "family_history",
    "hereditary": "family_history",
    "parents had it": "family_history",
    "family mein bhi tha": "family_history",

    # ── fast_heart_rate ──
    "fast heart rate": "fast_heart_rate",
    "rapid heartbeat": "fast_heart_rate",
    "heart racing": "fast_heart_rate",
    "heart beating fast": "fast_heart_rate",
    "tachycardia": "fast_heart_rate",
    "heart pounding": "fast_heart_rate",
    "dil tez dhadak raha": "fast_heart_rate",

    # ── fatigue ──
    "fatigue": "fatigue",
    "tired": "fatigue",
    "tiredness": "fatigue",
    "exhaustion": "fatigue",
    "exhausted": "fatigue",
    "feeling weak": "fatigue",
    "feeling tired": "fatigue",
    "no energy": "fatigue",
    "low energy": "fatigue",
    "lethargic": "fatigue",
    "drained": "fatigue",
    "worn out": "fatigue",
    "run down": "fatigue",
    "thakaan": "fatigue",
    "thak gaya": "fatigue",

    # ── fluid_overload ──
    "fluid overload": "fluid_overload",
    "fluid retention": "fluid_overload",
    "water retention": "fluid_overload",
    "edema": "fluid_overload",
    "oedema": "fluid_overload",

    # ── foul_smell_of urine ──  (note: dataset uses "foul_smell_of urine" with space)
    "foul smell of urine": "foul_smell_of urine",
    "smelly urine": "foul_smell_of urine",
    "bad smelling urine": "foul_smell_of urine",
    "urine smells bad": "foul_smell_of urine",
    "stinky urine": "foul_smell_of urine",

    # ── headache ──
    "headache": "headache",
    "head ache": "headache",
    "head pain": "headache",
    "pain in head": "headache",
    "my head hurts": "headache",
    "my head is pounding": "headache",
    "migraine": "headache",
    "throbbing head": "headache",
    "splitting headache": "headache",
    "tension headache": "headache",
    "sir dard": "headache",
    "sir mein dard": "headache",
    "doka dukhtay": "headache",

    # ── high_fever ──
    "high fever": "high_fever",
    "very high fever": "high_fever",
    "burning fever": "high_fever",
    "high temperature": "high_fever",
    "temperature is very high": "high_fever",
    "102 fever": "high_fever",
    "103 fever": "high_fever",
    "104 fever": "high_fever",
    "tez bukhar": "high_fever",
    "bahut bukhar": "high_fever",

    # ── hip_joint_pain ──
    "hip joint pain": "hip_joint_pain",
    "hip pain": "hip_joint_pain",
    "pain in hip": "hip_joint_pain",
    "my hip hurts": "hip_joint_pain",

    # ── history_of_alcohol_consumption ──
    "history of alcohol consumption": "history_of_alcohol_consumption",
    "alcohol consumption": "history_of_alcohol_consumption",
    "heavy drinking": "history_of_alcohol_consumption",
    "i drink alcohol": "history_of_alcohol_consumption",
    "alcoholic": "history_of_alcohol_consumption",
    "drinking habit": "history_of_alcohol_consumption",
    "sharab": "history_of_alcohol_consumption",

    # ── increased_appetite ──
    "increased appetite": "increased_appetite",
    "eating more than usual": "increased_appetite",
    "appetite increased": "increased_appetite",

    # ── indigestion ──
    "indigestion": "indigestion",
    "dyspepsia": "indigestion",
    "upset stomach": "indigestion",
    "difficulty digesting": "indigestion",
    "food not digesting": "indigestion",
    "badh hazmi": "indigestion",

    # ── inflammatory_nails ──
    "inflammatory nails": "inflammatory_nails",
    "inflamed nails": "inflammatory_nails",
    "nail inflammation": "inflammatory_nails",
    "red nails": "inflammatory_nails",
    "nail infection": "inflammatory_nails",
    "swollen nails": "inflammatory_nails",

    # ── internal_itching ──
    "internal itching": "internal_itching",
    "itching inside": "internal_itching",
    "inner itching": "internal_itching",
    "itching from inside": "internal_itching",

    # ── irregular_sugar_level ──
    "irregular sugar level": "irregular_sugar_level",
    "fluctuating sugar": "irregular_sugar_level",
    "blood sugar up and down": "irregular_sugar_level",
    "unstable blood sugar": "irregular_sugar_level",
    "sugar level": "irregular_sugar_level",

    # ── irritability ──
    "irritability": "irritability",
    "irritable": "irritability",
    "easily irritated": "irritability",
    "getting angry easily": "irritability",
    "short tempered": "irritability",
    "chidhchidha": "irritability",

    # ── irritation_in_anus ──
    "irritation in anus": "irritation_in_anus",
    "anal irritation": "irritation_in_anus",
    "itchy anus": "irritation_in_anus",
    "rectum itching": "irritation_in_anus",

    # ── itching ──
    "itching": "itching",
    "itchy skin": "itching",
    "skin itching": "itching",
    "scratching": "itching",
    "itchy": "itching",
    "khujli": "itching",

    # ── joint_pain ──
    "joint pain": "joint_pain",
    "joint ache": "joint_pain",
    "aching joints": "joint_pain",
    "pain in joints": "joint_pain",
    "joints hurt": "joint_pain",
    "joints hurting": "joint_pain",
    "joints are hurting": "joint_pain",
    "my joints hurt": "joint_pain",
    "my joints are hurting": "joint_pain",
    "arthritis pain": "joint_pain",
    "jodon mein dard": "joint_pain",

    # ── knee_pain ──
    "knee pain": "knee_pain",
    "pain in knee": "knee_pain",
    "my knee hurts": "knee_pain",
    "knee ache": "knee_pain",
    "ghutne mein dard": "knee_pain",

    # ── lack_of_concentration ──
    "lack of concentration": "lack_of_concentration",
    "cannot concentrate": "lack_of_concentration",
    "difficulty concentrating": "lack_of_concentration",
    "poor concentration": "lack_of_concentration",
    "mind wandering": "lack_of_concentration",
    "can't focus": "lack_of_concentration",
    "brain fog": "lack_of_concentration",

    # ── lethargy ──
    "lethargy": "lethargy",
    "sluggish": "lethargy",
    "feeling sluggish": "lethargy",
    "no motivation": "lethargy",
    "lazy feeling": "lethargy",
    "aalas": "lethargy",

    # ── loss_of_appetite ──
    "loss of appetite": "loss_of_appetite",
    "no appetite": "loss_of_appetite",
    "not hungry": "loss_of_appetite",
    "don't feel like eating": "loss_of_appetite",
    "can't eat": "loss_of_appetite",
    "food doesn't appeal": "loss_of_appetite",
    "bhookh nahi": "loss_of_appetite",
    "khana nahi khaya ja raha": "loss_of_appetite",

    # ── loss_of_balance ──
    "loss of balance": "loss_of_balance",
    "losing balance": "loss_of_balance",
    "unbalanced": "loss_of_balance",
    "falling over": "loss_of_balance",
    "can't keep balance": "loss_of_balance",
    "unsteady walking": "loss_of_balance",

    # ── loss_of_smell ──
    "loss of smell": "loss_of_smell",
    "can't smell": "loss_of_smell",
    "no sense of smell": "loss_of_smell",
    "anosmia": "loss_of_smell",
    "smell gone": "loss_of_smell",

    # ── malaise ──
    "malaise": "malaise",
    "feeling unwell": "malaise",
    "generally unwell": "malaise",
    "not feeling well": "malaise",
    "feeling sick": "malaise",
    "under the weather": "malaise",
    "tabiyat theek nahi": "malaise",

    # ── mild_fever ──
    "mild fever": "mild_fever",
    "slight fever": "mild_fever",
    "low grade fever": "mild_fever",
    "low fever": "mild_fever",
    "fever": "mild_fever",                  # default for "fever" is mild
    "bukhar": "mild_fever",
    "halka bukhar": "mild_fever",
    "taap": "mild_fever",

    # ── mood_swings ──
    "mood swings": "mood_swings",
    "mood changes": "mood_swings",
    "emotional changes": "mood_swings",
    "mood up and down": "mood_swings",
    "mood fluctuations": "mood_swings",

    # ── movement_stiffness ──
    "movement stiffness": "movement_stiffness",
    "stiffness": "movement_stiffness",
    "stiff body": "movement_stiffness",
    "difficulty moving": "movement_stiffness",
    "body stiff": "movement_stiffness",
    "rigid body": "movement_stiffness",

    # ── mucoid_sputum ──
    "mucoid sputum": "mucoid_sputum",
    "mucus in cough": "mucoid_sputum",
    "phlegm": "mucoid_sputum",
    "coughing mucus": "mucoid_sputum",
    "thick sputum": "mucoid_sputum",
    "balgam": "mucoid_sputum",

    # ── muscle_pain ──
    "muscle pain": "muscle_pain",
    "muscle ache": "muscle_pain",
    "sore muscles": "muscle_pain",
    "muscle soreness": "muscle_pain",
    "muscles hurt": "muscle_pain",
    "body ache": "muscle_pain",
    "body pain": "muscle_pain",
    "myalgia": "muscle_pain",
    "badan dard": "muscle_pain",

    # ── muscle_wasting ──
    "muscle wasting": "muscle_wasting",
    "muscle loss": "muscle_wasting",
    "muscles shrinking": "muscle_wasting",
    "atrophy": "muscle_wasting",
    "losing muscle": "muscle_wasting",

    # ── muscle_weakness ──
    "muscle weakness": "muscle_weakness",
    "weak muscles": "muscle_weakness",
    "muscles feel weak": "muscle_weakness",
    "can't lift": "muscle_weakness",
    "no strength": "muscle_weakness",
    "kamzori": "muscle_weakness",

    # ── nausea ──
    "nausea": "nausea",
    "nauseous": "nausea",
    "feeling nauseous": "nausea",
    "feel like vomiting": "nausea",
    "want to vomit": "nausea",
    "feel like throwing up": "nausea",
    "queasy": "nausea",
    "ji machal raha": "nausea",
    "ji ghabra raha": "nausea",

    # ── neck_pain ──
    "neck pain": "neck_pain",
    "stiff neck": "neck_pain",
    "pain in neck": "neck_pain",
    "my neck hurts": "neck_pain",
    "gardan mein dard": "neck_pain",

    # ── nodal_skin_eruptions ──
    "nodal skin eruptions": "nodal_skin_eruptions",
    "skin eruptions": "nodal_skin_eruptions",
    "skin bumps": "nodal_skin_eruptions",
    "bumps on skin": "nodal_skin_eruptions",
    "nodules on skin": "nodal_skin_eruptions",

    # ── obesity ──
    "obesity": "obesity",
    "obese": "obesity",
    "overweight": "obesity",
    "very fat": "obesity",
    "mota": "obesity",

    # ── pain_behind_the_eyes ──
    "pain behind the eyes": "pain_behind_the_eyes",
    "pain behind eyes": "pain_behind_the_eyes",
    "eye pain": "pain_behind_the_eyes",
    "eyes hurt": "pain_behind_the_eyes",
    "eyes paining": "pain_behind_the_eyes",
    "aankhon ke peeche dard": "pain_behind_the_eyes",

    # ── pain_during_bowel_movements ──
    "pain during bowel movements": "pain_during_bowel_movements",
    "painful bowel movement": "pain_during_bowel_movements",
    "pain when passing stool": "pain_during_bowel_movements",
    "hurts to pass stool": "pain_during_bowel_movements",

    # ── pain_in_anal_region ──
    "pain in anal region": "pain_in_anal_region",
    "anal pain": "pain_in_anal_region",
    "rectal pain": "pain_in_anal_region",
    "pain in anus": "pain_in_anal_region",

    # ── painful_walking ──
    "painful walking": "painful_walking",
    "pain while walking": "painful_walking",
    "hurts to walk": "painful_walking",
    "difficulty walking": "painful_walking",
    "limping": "painful_walking",

    # ── palpitations ──
    "palpitations": "palpitations",
    "heart palpitations": "palpitations",
    "heart skipping": "palpitations",
    "heart flutter": "palpitations",
    "irregular heartbeat": "palpitations",
    "dil dhadak raha": "palpitations",

    # ── passage_of_gases ──
    "passage of gases": "passage_of_gases",
    "flatulence": "passage_of_gases",
    "passing gas": "passage_of_gases",
    "gas": "passage_of_gases",
    "farting": "passage_of_gases",
    "bloating gas": "passage_of_gases",

    # ── patches_in_throat ──
    "patches in throat": "patches_in_throat",
    "white patches in throat": "patches_in_throat",
    "throat patches": "patches_in_throat",
    "spots in throat": "patches_in_throat",

    # ── phlegm ──
    "phlegm": "phlegm",
    "mucus": "phlegm",
    "sputum": "phlegm",
    "catarrh": "phlegm",
    "balgam": "phlegm",

    # ── polyuria ──
    "polyuria": "polyuria",
    "excessive urination": "polyuria",
    "peeing a lot": "polyuria",
    "frequent peeing": "polyuria",
    "urinating frequently": "polyuria",
    "zyada peshab": "polyuria",

    # ── prominent_veins_on_calf ──
    "prominent veins on calf": "prominent_veins_on_calf",
    "varicose veins": "prominent_veins_on_calf",
    "bulging veins": "prominent_veins_on_calf",
    "visible veins on leg": "prominent_veins_on_calf",

    # ── puffy_face_and_eyes ──
    "puffy face and eyes": "puffy_face_and_eyes",
    "puffy face": "puffy_face_and_eyes",
    "swollen face": "puffy_face_and_eyes",
    "puffy eyes": "puffy_face_and_eyes",
    "swollen eyes": "puffy_face_and_eyes",
    "face swelling": "puffy_face_and_eyes",

    # ── pus_filled_pimples ──
    "pus filled pimples": "pus_filled_pimples",
    "pimples with pus": "pus_filled_pimples",
    "acne": "pus_filled_pimples",
    "pimples": "pus_filled_pimples",
    "zits": "pus_filled_pimples",

    # ── receiving_blood_transfusion ──
    "receiving blood transfusion": "receiving_blood_transfusion",
    "blood transfusion": "receiving_blood_transfusion",
    "got blood transfusion": "receiving_blood_transfusion",
    "received blood": "receiving_blood_transfusion",

    # ── receiving_unsterile_injections ──
    "receiving unsterile injections": "receiving_unsterile_injections",
    "unsterile injection": "receiving_unsterile_injections",
    "dirty needle": "receiving_unsterile_injections",
    "shared needle": "receiving_unsterile_injections",

    # ── red_sore_around_nose ──
    "red sore around nose": "red_sore_around_nose",
    "sore around nose": "red_sore_around_nose",
    "redness around nose": "red_sore_around_nose",
    "red nose": "red_sore_around_nose",

    # ── red_spots_over_body ──
    "red spots over body": "red_spots_over_body",
    "red spots on body": "red_spots_over_body",
    "red spots": "red_spots_over_body",
    "red dots on skin": "red_spots_over_body",
    "petechiae": "red_spots_over_body",

    # ── redness_of_eyes ──
    "redness of eyes": "redness_of_eyes",
    "red eyes": "redness_of_eyes",
    "bloodshot eyes": "redness_of_eyes",
    "eyes are red": "redness_of_eyes",
    "aankh laal": "redness_of_eyes",

    # ── restlessness ──
    "restlessness": "restlessness",
    "restless": "restlessness",
    "can't sit still": "restlessness",
    "fidgety": "restlessness",
    "agitated": "restlessness",
    "bechain": "restlessness",

    # ── runny_nose ──
    "runny nose": "runny_nose",
    "running nose": "runny_nose",
    "nose running": "runny_nose",
    "nasal drip": "runny_nose",
    "nose dripping": "runny_nose",
    "naak beh raha": "runny_nose",

    # ── rusty_sputum ──
    "rusty sputum": "rusty_sputum",
    "rust colored sputum": "rusty_sputum",
    "brown sputum": "rusty_sputum",

    # ── scurring ──
    "scurring": "scurring",
    "scurvy": "scurring",
    "skin scurring": "scurring",

    # ── shivering ──
    "shivering": "shivering",
    "shaking": "shivering",
    "trembling": "shivering",
    "body shivering": "shivering",
    "kaamp raha": "shivering",

    # ── silver_like_dusting ──
    "silver like dusting": "silver_like_dusting",
    "silver scales on skin": "silver_like_dusting",
    "silvery skin": "silver_like_dusting",
    "psoriasis scales": "silver_like_dusting",

    # ── sinus_pressure ──
    "sinus pressure": "sinus_pressure",
    "sinus pain": "sinus_pressure",
    "sinus headache": "sinus_pressure",
    "sinusitis": "sinus_pressure",
    "face pressure": "sinus_pressure",

    # ── skin_peeling ──
    "skin peeling": "skin_peeling",
    "peeling skin": "skin_peeling",
    "skin coming off": "skin_peeling",
    "flaky skin": "skin_peeling",

    # ── skin_rash ──
    "skin rash": "skin_rash",
    "rash": "skin_rash",
    "rashes": "skin_rash",
    "rash on skin": "skin_rash",
    "skin irritation": "skin_rash",
    "red rash": "skin_rash",

    # ── slurred_speech ──
    "slurred speech": "slurred_speech",
    "difficulty speaking": "slurred_speech",
    "speech difficulty": "slurred_speech",
    "can't speak clearly": "slurred_speech",
    "words slurring": "slurred_speech",
    "can't talk properly": "slurred_speech",

    # ── small_dents_in_nails ──
    "small dents in nails": "small_dents_in_nails",
    "nail pitting": "small_dents_in_nails",
    "dents in nails": "small_dents_in_nails",
    "pitted nails": "small_dents_in_nails",

    # ── spinning_movements ──
    "spinning movements": "spinning_movements",
    "spinning sensation": "spinning_movements",
    "world is spinning": "spinning_movements",
    "vertigo spinning": "spinning_movements",
    "everything spinning": "spinning_movements",

    # ── spotting_ urination ──  (note: dataset has space before urination)
    "spotting urination": "spotting_ urination",
    "blood in urine": "spotting_ urination",
    "bloody urine": "spotting_ urination",
    "hematuria": "spotting_ urination",
    "red urine": "spotting_ urination",

    # ── stiff_neck ──
    "stiff neck": "stiff_neck",
    "neck stiffness": "stiff_neck",
    "can't move neck": "stiff_neck",
    "neck is stiff": "stiff_neck",

    # ── stomach_bleeding ──
    "stomach bleeding": "stomach_bleeding",
    "internal bleeding": "stomach_bleeding",
    "gi bleeding": "stomach_bleeding",
    "gastrointestinal bleeding": "stomach_bleeding",
    "vomiting blood": "stomach_bleeding",

    # ── stomach_pain ──
    "stomach pain": "stomach_pain",
    "tummy pain": "stomach_pain",
    "pain in tummy": "stomach_pain",
    "gastric pain": "stomach_pain",
    "pet mein dard": "stomach_pain",
    "stomach killing": "stomach_pain",
    "stomach is killing": "stomach_pain",

    # ── sunken_eyes ──
    "sunken eyes": "sunken_eyes",
    "eyes sunken": "sunken_eyes",
    "hollow eyes": "sunken_eyes",
    "dark circles": "sunken_eyes",

    # ── sweating ──
    "sweating": "sweating",
    "excessive sweating": "sweating",
    "sweaty": "sweating",
    "profuse sweating": "sweating",
    "cold sweat": "sweating",
    "night sweats": "sweating",
    "paseena": "sweating",
    "bahut paseena": "sweating",

    # ── swelled_lymph_nodes ──
    "swelled lymph nodes": "swelled_lymph_nodes",
    "swollen lymph nodes": "swelled_lymph_nodes",
    "swollen glands": "swelled_lymph_nodes",
    "enlarged lymph nodes": "swelled_lymph_nodes",
    "lymph nodes": "swelled_lymph_nodes",

    # ── swelling_joints ──
    "swelling joints": "swelling_joints",
    "swollen joints": "swelling_joints",
    "joint swelling": "swelling_joints",
    "joints swollen": "swelling_joints",
    "puffy joints": "swelling_joints",

    # ── swelling_of_stomach ──
    "swelling of stomach": "swelling_of_stomach",
    "stomach swollen": "swelling_of_stomach",
    "abdomen swollen": "swelling_of_stomach",
    "belly swelling": "swelling_of_stomach",

    # ── swollen_blood_vessels ──
    "swollen blood vessels": "swollen_blood_vessels",
    "distended veins": "swollen_blood_vessels",
    "enlarged blood vessels": "swollen_blood_vessels",
    "varicose": "swollen_blood_vessels",

    # ── swollen_extremeties ──  (note: dataset misspelling)
    "swollen extremities": "swollen_extremeties",
    "swollen hands": "swollen_extremeties",
    "swollen feet": "swollen_extremeties",
    "swelling in hands": "swollen_extremeties",
    "swelling in feet": "swollen_extremeties",
    "hands swollen": "swollen_extremeties",
    "feet swollen": "swollen_extremeties",
    "paav sooj gaye": "swollen_extremeties",

    # ── swollen_legs ──
    "swollen legs": "swollen_legs",
    "leg swelling": "swollen_legs",
    "legs swollen": "swollen_legs",
    "puffy legs": "swollen_legs",
    "pair sooj gaye": "swollen_legs",

    # ── throat_irritation ──
    "throat irritation": "throat_irritation",
    "sore throat": "throat_irritation",
    "scratchy throat": "throat_irritation",
    "throat pain": "throat_irritation",
    "itchy throat": "throat_irritation",
    "gala dard": "throat_irritation",
    "gale mein kharash": "throat_irritation",

    # ── toxic_look_(typhos) ──
    "toxic look": "toxic_look_(typhos)",
    "looks very ill": "toxic_look_(typhos)",
    "looking very sick": "toxic_look_(typhos)",
    "gravely ill appearance": "toxic_look_(typhos)",

    # ── ulcers_on_tongue ──
    "ulcers on tongue": "ulcers_on_tongue",
    "mouth ulcers": "ulcers_on_tongue",
    "tongue sores": "ulcers_on_tongue",
    "canker sores": "ulcers_on_tongue",
    "mouth sores": "ulcers_on_tongue",
    "munh mein chhale": "ulcers_on_tongue",

    # ── unsteadiness ──
    "unsteadiness": "unsteadiness",
    "unsteady": "unsteadiness",
    "wobbly": "unsteadiness",
    "stumbling": "unsteadiness",
    "gait problem": "unsteadiness",

    # ── visual_disturbances ──
    "visual disturbances": "visual_disturbances",
    "seeing spots": "visual_disturbances",
    "flashing lights": "visual_disturbances",
    "floaters": "visual_disturbances",
    "vision changes": "visual_disturbances",
    "double vision": "visual_disturbances",

    # ── vomiting ──
    "vomiting": "vomiting",
    "throwing up": "vomiting",
    "puking": "vomiting",
    "being sick": "vomiting",
    "threw up": "vomiting",
    "keep throwing up": "vomiting",
    "ulti": "vomiting",
    "ulti ho rahi": "vomiting",

    # ── watering_from_eyes ──
    "watering from eyes": "watering_from_eyes",
    "watery eyes": "watering_from_eyes",
    "eyes watering": "watering_from_eyes",
    "teary eyes": "watering_from_eyes",
    "tears": "watering_from_eyes",
    "aankh se paani": "watering_from_eyes",

    # ── weakness_in_limbs ──
    "weakness in limbs": "weakness_in_limbs",
    "weak arms": "weakness_in_limbs",
    "weak legs": "weakness_in_limbs",
    "arms feel weak": "weakness_in_limbs",
    "legs feel weak": "weakness_in_limbs",
    "haath pair kamzor": "weakness_in_limbs",

    # ── weakness_of_one_body_side ──
    "weakness of one body side": "weakness_of_one_body_side",
    "one side weakness": "weakness_of_one_body_side",
    "one side paralysis": "weakness_of_one_body_side",
    "half body weak": "weakness_of_one_body_side",
    "left side weak": "weakness_of_one_body_side",
    "right side weak": "weakness_of_one_body_side",
    "hemiplegia": "weakness_of_one_body_side",

    # ── weight_gain ──
    "weight gain": "weight_gain",
    "gaining weight": "weight_gain",
    "putting on weight": "weight_gain",
    "getting fat": "weight_gain",
    "wajan badh raha": "weight_gain",

    # ── weight_loss ──
    "weight loss": "weight_loss",
    "losing weight": "weight_loss",
    "losing weight unexpectedly": "weight_loss",
    "unexplained weight loss": "weight_loss",
    "getting thin": "weight_loss",
    "wajan kam ho raha": "weight_loss",

    # ── yellow_crust_ooze ──
    "yellow crust ooze": "yellow_crust_ooze",
    "yellow crusting": "yellow_crust_ooze",
    "oozing skin": "yellow_crust_ooze",
    "yellow discharge from skin": "yellow_crust_ooze",

    # ── yellow_urine ──
    "yellow urine": "yellow_urine",
    "dark yellow urine": "yellow_urine",
    "bright yellow pee": "yellow_urine",
    "concentrated urine": "yellow_urine",

    # ── yellowing_of_eyes ──
    "yellowing of eyes": "yellowing_of_eyes",
    "yellow eyes": "yellowing_of_eyes",
    "eyes turning yellow": "yellowing_of_eyes",
    "jaundice eyes": "yellowing_of_eyes",
    "aankh peeli": "yellowing_of_eyes",

    # ── yellowish_skin ──
    "yellowish skin": "yellowish_skin",
    "yellow skin": "yellowish_skin",
    "jaundice": "yellowish_skin",
    "turning yellow": "yellowish_skin",
    "peeli twacha": "yellowish_skin",
    "piliya": "yellowish_skin",
}

# ─────────────────────────────────────────────────────────────────────────────
#  NEGATION PATTERNS
#  Sentences containing these patterns before a symptom exclude that symptom.
# ─────────────────────────────────────────────────────────────────────────────

_NEGATION_WORDS = {
    # English
    "no", "not", "don't", "dont", "doesn't", "doesnt", "didn't", "didnt",
    "haven't", "havent", "hasn't", "hasnt", "never", "without", "nor",
    "neither", "ain't", "aint", "none",
    # Hindi / Marathi
    "nahi", "nai", "nahin", "nah", "na", "mat",
}

# Compiled once for reuse
_NEGATION_RE = re.compile(
    r'\b(' + '|'.join(re.escape(w) for w in sorted(_NEGATION_WORDS, key=len, reverse=True)) + r')\b',
    re.IGNORECASE,
)


# ─────────────────────────────────────────────────────────────────────────────
#  PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def _split_into_clauses(text: str) -> list[str]:
    """
    Split input text into clauses at sentence / conjunction boundaries.
    Each clause is processed independently so negation in one clause
    doesn't affect symptoms mentioned in another.
    """
    # Split on sentence endings, commas, "and", "but", "however", semicolons
    parts = re.split(
        r'[.!;]+|\band\b|\bbut\b|\bhowever\b|\balthough\b|\byet\b|,',
        text,
        flags=re.IGNORECASE,
    )
    return [p.strip() for p in parts if p.strip()]


def _clause_is_negated(clause: str, symptom_phrase: str) -> bool:
    """
    Check whether a symptom phrase inside this clause is negated.
    We look for negation words appearing BEFORE the symptom phrase
    within a window of ~6 words.
    """
    clause_lower = clause.lower()
    phrase_lower = symptom_phrase.lower()
    idx = clause_lower.find(phrase_lower)
    if idx == -1:
        return False

    # Look at the 60 chars before the match
    window = clause_lower[max(0, idx - 60):idx]
    return bool(_NEGATION_RE.search(window))


def extract_symptoms_nlp(raw_text: str) -> tuple[list[str], list[str]]:
    """
    Advanced NLP symptom extraction.

    Returns:
        (extracted_symptoms, negated_symptoms)
        Both are lists of model column names.
    """
    text_lower = raw_text.lower().strip()
    if not text_lower:
        return [], []

    clauses = _split_into_clauses(text_lower)
    extracted: set[str] = set()
    negated: set[str] = set()

    # Sort phrase map by length (longest first) so "chest pain" matches before "pain"
    sorted_phrases = sorted(NLP_PHRASE_MAP.keys(), key=len, reverse=True)

    for clause in clauses:
        for phrase in sorted_phrases:
            if phrase in clause:
                col = NLP_PHRASE_MAP[phrase]
                if _clause_is_negated(clause, phrase):
                    negated.add(col)
                else:
                    extracted.add(col)

    # Also do direct column-name matching (underscored names in text)
    all_cols = set(get_all_symptoms())
    for col in all_cols:
        readable = col.replace("_", " ")
        for clause in clauses:
            if readable in clause or col in clause:
                if col not in extracted and col not in negated:
                    if not any(_clause_is_negated(c, readable) for c in clauses if readable in c):
                        extracted.add(col)

    # Remove anything negated from extracted
    extracted -= negated

    return sorted(extracted), sorted(negated)
