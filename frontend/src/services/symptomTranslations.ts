/**
 * Symptom translations for Hindi and Marathi
 * Synced with backend translations.py
 */

type Language = 'en' | 'hi' | 'mr';

const SYMPTOM_TRANSLATIONS: Record<string, Record<Language, string>> = {
  abdominal_pain: { en: 'Abdominal Pain', hi: 'पेट में दर्द', mr: 'ओटीपी दर्द' },
  abnormal_menstruation: { en: 'Abnormal Menstruation', hi: 'असामान्य मासिक धर्म', mr: 'असामान्य मासिक धर्म' },
  acidity: { en: 'Acidity', hi: 'अम्लता', mr: 'आम्लता' },
  anxiety: { en: 'Anxiety', hi: 'चिंता', mr: 'चिंता' },
  back_pain: { en: 'Back Pain', hi: 'पीठ दर्द', mr: 'पाठीचा दर्द' },
  belly_pain: { en: 'Belly Pain', hi: 'पेट का दर्द', mr: 'पोटीचा दर्द' },
  blackheads: { en: 'Blackheads', hi: 'काले धब्बे', mr: 'काळे डाग' },
  bladder_discomfort: { en: 'Bladder Discomfort', hi: 'मूत्राशय में असुविधा', mr: 'मूत्राशयात असुविधा' },
  blister: { en: 'Blister', hi: 'छाले', mr: 'फुगा' },
  blood_in_sputum: { en: 'Blood in Sputum', hi: 'थूक में रक्त', mr: 'थुंकीत रक्त' },
  bloody_stool: { en: 'Bloody Stool', hi: 'खूनी मल', mr: 'रक्त युक्त मल' },
  blurred_and_distorted_vision: { en: 'Blurred & Distorted Vision', hi: 'धुंधली और विकृत दृष्टि', mr: 'अस्पष्ट आणि विकृत दृष्टि' },
  breathlessness: { en: 'Breathlessness', hi: 'सांस की कमी', mr: 'श्वासकष्ट' },
  brittle_nails: { en: 'Brittle Nails', hi: 'नाजुक नाखून', mr: 'नाजूक नखे' },
  bruising: { en: 'Bruising', hi: 'चोट के निशान', mr: 'जखमी चिन्हे' },
  burning_micturition: { en: 'Burning Micturition', hi: 'पेशाब में जलन', mr: 'पेशाब करताना जळजळ' },
  chest_pain: { en: 'Chest Pain', hi: 'छाती में दर्द', mr: 'छातीचा दर्द' },
  chills: { en: 'Chills', hi: 'ठंड लगना', mr: 'कंपकंपी' },
  cold_hands_and_feets: { en: 'Cold Hands & Feet', hi: 'ठंडे हाथ और पैर', mr: 'थंड हात आणि पाय' },
  coma: { en: 'Coma', hi: 'कोमा', mr: 'कोमा' },
  congestion: { en: 'Congestion', hi: 'भीड़ा', mr: 'भाग भरणे' },
  constipation: { en: 'Constipation', hi: 'कब्ज', mr: 'कोष्ठबद्धता' },
  continuous_sneezing: { en: 'Continuous Sneezing', hi: 'लगातार छींक', mr: 'सतत शिंकणे' },
  cough: { en: 'Cough', hi: 'खांसी', mr: 'खोकला' },
  cramps: { en: 'Cramps', hi: 'ऐंठन', mr: 'ऐठण' },
  dark_urine: { en: 'Dark Urine', hi: 'गहरा मूत्र', mr: 'गडद मूत्र' },
  dehydration: { en: 'Dehydration', hi: 'निर्जलीकरण', mr: 'निर्जलीकरण' },
  depression: { en: 'Depression', hi: 'अवसाद', mr: 'नैराश्य' },
  diarrhoea: { en: 'Diarrhoea', hi: 'दस्त', mr: 'दस्त' },
  dizziness: { en: 'Dizziness', hi: 'चक्कर आना', mr: 'चक्कर' },
  enlarged_thyroid: { en: 'Enlarged Thyroid', hi: 'बड़ी थायरॉयड', mr: 'वाढलेली थायरॉइड' },
  excessive_hunger: { en: 'Excessive Hunger', hi: 'अत्यधिक भूख', mr: 'अत्यधिक भूक' },
  fatigue: { en: 'Fatigue', hi: 'थकावट', mr: 'थकवा' },
  fast_heart_rate: { en: 'Fast Heart Rate', hi: 'तेज़ दिल की गति', mr: 'वेगवान हृदय गति' },
  headache: { en: 'Headache', hi: 'सिरदर्द', mr: 'डोकेदुखी' },
  high_fever: { en: 'High Fever', hi: 'तेज़ बुखार', mr: 'उच्च ताप' },
  hip_joint_pain: { en: 'Hip Joint Pain', hi: 'कूल्हे का जोड़ दर्द', mr: 'हिप संयुक्त दर्द' },
  indigestion: { en: 'Indigestion', hi: 'अपच', mr: 'अजीर्ण' },
  irritability: { en: 'Irritability', hi: 'चिड़चिड़ापन', mr: 'रुचीरुदरता' },
  itching: { en: 'Itching', hi: 'खुजली', mr: 'खाज' },
  joint_pain: { en: 'Joint Pain', hi: 'जोड़ों में दर्द', mr: 'संयुक्त दर्द' },
  knee_pain: { en: 'Knee Pain', hi: 'घुटने में दर्द', mr: 'गुडघ्याचा दर्द' },
  lack_of_concentration: { en: 'Lack of Concentration', hi: 'ध्यान की कमी', mr: 'एकाग्रता की कमी' },
  lethargy: { en: 'Lethargy', hi: 'सुस्ती', mr: 'सुस्ती' },
  loss_of_appetite: { en: 'Loss of Appetite', hi: 'भूख न लगना', mr: 'भुक्षेच्या नुकसान' },
  loss_of_balance: { en: 'Loss of Balance', hi: 'संतुलन खोना', mr: 'संतुलन हरणे' },
  loss_of_smell: { en: 'Loss of Smell', hi: 'गंध खोना', mr: 'वास हरणे' },
  malaise: { en: 'Malaise', hi: 'बीमारी की अनुभूति', mr: 'अस्वस्थता' },
  mild_fever: { en: 'Mild Fever', hi: 'हल्का बुखार', mr: 'हलका ताप' },
  mood_swings: { en: 'Mood Swings', hi: 'मनोदशा में बदलाव', mr: 'मनस्थितीत बदल' },
  movement_stiffness: { en: 'Movement Stiffness', hi: 'आंदोलन की कठोरता', mr: 'हालचाली कठोरता' },
  muscle_pain: { en: 'Muscle Pain', hi: 'मांसपेशियों में दर्द', mr: 'स्नायु दर्द' },
  muscle_weakness: { en: 'Muscle Weakness', hi: 'मांसपेशियों में कमजोरी', mr: 'स्नायु कमजोरी' },
  muscle_wasting: { en: 'Muscle Wasting', hi: 'मांसपेशियों की बर्बादी', mr: 'स्नायु क्षय' },
  nausea: { en: 'Nausea', hi: 'मतली', mr: 'अरुची' },
  neck_pain: { en: 'Neck Pain', hi: 'गर्दन में दर्द', mr: 'मानेचा दर्द' },
  nodal_skin_eruptions: { en: 'Nodal Skin Eruptions', hi: 'नोडल त्वचा विस्फोट', mr: 'नोडल त्वचा उद्रेक' },
  obesity: { en: 'Obesity', hi: 'मोटापा', mr: 'स्थूलता' },
  pain_behind_the_eyes: { en: 'Pain Behind Eyes', hi: 'आंखों के पीछे दर्द', mr: 'डोळ्यांच्या मागे दर्द' },
  palpitations: { en: 'Palpitations', hi: 'धड़कन', mr: 'दिलचस्पी' },
  phlegm: { en: 'Phlegm', hi: 'कफ', mr: 'कफ' },
  polyuria: { en: 'Polyuria', hi: 'अत्यधिक पेशाब', mr: 'अत्यधिक मूत्र' },
  puffy_face_and_eyes: { en: 'Puffy Face & Eyes', hi: 'सूजा हुआ चेहरा और आंखें', mr: 'फुगांचा चेहरा आणि डोळे' },
  restlessness: { en: 'Restlessness', hi: 'बेचैनी', mr: 'अस्थिरता' },
  runny_nose: { en: 'Runny Nose', hi: 'नाक बहना', mr: 'नाक वाहत' },
  skin_rash: { en: 'Skin Rash', hi: 'त्वचा पर लाल चकत्ते', mr: 'त्वचा रज' },
  skin_peeling: { en: 'Skin Peeling', hi: 'त्वचा छिलना', mr: 'त्वचा सोलून' },
  slurred_speech: { en: 'Slurred Speech', hi: 'अस्पष्ट भाषण', mr: 'अस्पष्ट भाषण' },
  shivering: { en: 'Shivering', hi: 'कंपकंपी', mr: 'कंपकंपी' },
  stomach_pain: { en: 'Stomach Pain', hi: 'पेट में दर्द', mr: 'पोटीचा दर्द' },
  sweating: { en: 'Sweating', hi: 'पसीना', mr: 'घाम' },
  swelling_joints: { en: 'Swelling Joints', hi: 'जोड़ों में सूजन', mr: 'सूजलेले संयुक्त' },
  swollen_legs: { en: 'Swollen Legs', hi: 'सूजे हुए पैर', mr: 'सूजलेले पाय' },
  throat_irritation: { en: 'Throat Irritation', hi: 'गले में जलन', mr: 'घसरणीची जळजळ' },
  ulcers_on_tongue: { en: 'Ulcers on Tongue', hi: 'जीभ पर छाले', mr: 'जिभेवर पोपळे' },
  visual_disturbances: { en: 'Visual Disturbances', hi: 'दृश्य विकार', mr: 'दृश्य व्यतिक्रमण' },
  vomiting: { en: 'Vomiting', hi: 'उल्टी', mr: 'मळमळ' },
  watering_from_eyes: { en: 'Watering from Eyes', hi: 'आंखों से पानी बहना', mr: 'डोळ्यांमधून पाणी' },
  weakness_in_limbs: { en: 'Weakness in Limbs', hi: 'अंगों में कमजोरी', mr: 'अंगांमध्ये कमजोरी' },
  weight_gain: { en: 'Weight Gain', hi: 'वजन बढ़ना', mr: 'वजन वाढ' },
  weight_loss: { en: 'Weight Loss', hi: 'वजन घटना', mr: 'वजन हरणे' },
  yellow_urine: { en: 'Yellow Urine', hi: 'पीला मूत्र', mr: 'पिवळ मूत्र' },
  yellowing_of_eyes: { en: 'Yellowing of Eyes', hi: 'आंखों का पीला पड़ना', mr: 'डोळ्यांचा पिवळसर' },
  yellowish_skin: { en: 'Yellowish Skin', hi: 'पीली त्वचा', mr: 'पिवळ त्वचा' },
};

export function translateSymptom(symptomId: string, language: Language): string {
  const translations = SYMPTOM_TRANSLATIONS[symptomId];
  if (!translations) {
    // Fallback: format the ID
    return symptomId.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }
  return translations[language] || translations.en;
}

export function getTranslatedSymptomName(symptomId: string, language: Language): string {
  return translateSymptom(symptomId, language);
}
