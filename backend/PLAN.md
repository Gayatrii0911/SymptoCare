# 🧠 AI Health Triage Copilot – Full-Stack Architecture & Implementation Plan

> **Project:** Avalon – AI-Powered Health Symptom Triage & Risk Assessment  
> **Stack:** Flask (Python) + React (TypeScript) + Naive Bayes ML Model  
> **Deployment:** Local demo  
> **Last Updated:** 2026-02-11

---

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        REACT FRONTEND                          │
│  (Vite + TypeScript + Tailwind CSS + Framer Motion)            │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │ Symptom  │ │  Risk    │ │ History  │ │ Voice Input      │  │
│  │ Selector │ │Dashboard │ │ Records  │ │ (Web Speech API) │  │
│  └────┬─────┘ └────▲─────┘ └──────────┘ └──────────────────┘  │
│       │             │                                           │
│       ▼             │                                           │
│  ┌──────────────────┴──────────────────┐                       │
│  │       API Service (Axios/Fetch)     │                       │
│  └──────────────────┬──────────────────┘                       │
│                     │  HTTP (JSON)                              │
└─────────────────────┼──────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────┴──────────────────────────────────────────┐
│                      FLASK BACKEND (API)                       │
│                                                                 │
│  ┌─────────┐    ┌──────────────────────────────────────────┐   │
│  │ routes  │───▶│          TRIAGE PIPELINE                 │   │
│  │  .py    │    │                                          │   │
│  └─────────┘    │  Phase 1: Input Parsing & Normalization  │   │
│                 │  Phase 2: Symptom Neglect Detection       │   │
│                 │  Phase 3: Silent Emergency Detection      │   │
│                 │  Phase 4: Risk Classification (ML + Rules)│   │
│                 │  Phase 5: Explainability Narratives       │   │
│                 │  Phase 6: Outcome Awareness               │   │
│                 │  Phase 7: Actionable Recommendations      │   │
│                 │  Phase 8: Caregiver Escalation             │   │
│                 │  Phase 9: Multilingual Response            │   │
│                 └──────────────┬─────────────────────────────┘  │
│                                │                                │
│                 ┌──────────────▼─────────────────┐             │
│                 │   ML MODEL (Naive Bayes .pkl)  │             │
│                 │   + Knowledge Base (rules)     │             │
│                 └────────────────────────────────┘             │
└────────────────────────────────────────────────────────────────┘
```

---

## 📁 Full Project Folder Structure

```
Avalon/
│
├── backend/                              # Flask API Server
│   ├── run.py                            # Entry point
│   ├── requirements.txt                  # Python dependencies
│   ├── PLAN.md                           # This file
│   ├── dataset.csv                       # Training dataset (symptoms → disease)
│   │
│   ├── ml/                               # Machine Learning layer
│   │   ├── __init__.py
│   │   ├── train_model.py                # Script to train Naive Bayes from CSV
│   │   ├── predictor.py                  # Load model & predict disease/risk
│   │   ├── model.pkl                     # Trained Naive Bayes model
│   │   ├── label_encoder.pkl             # Label encoder for disease names
│   │   └── symptom_columns.pkl           # Feature column names (ordered)
│   │
│   ├── app/
│   │   ├── __init__.py                   # Flask app factory
│   │   ├── config.py                     # Configuration
│   │   ├── models.py                     # Data classes (TriageInput, TriageResult)
│   │   ├── routes.py                     # API endpoints
│   │   │
│   │   └── engine/                       # Triage pipeline (Phase 1–9)
│   │       ├── __init__.py
│   │       ├── knowledge_base.py         # Symptom maps, risk clusters, patterns
│   │       ├── phase1_input.py           # Input parsing & normalization
│   │       ├── phase2_neglect.py         # Symptom neglect detection
│   │       ├── phase3_silent.py          # Silent emergency detection
│   │       ├── phase4_risk.py            # Risk classification (ML + rules)
│   │       ├── phase5_explain.py         # Explainability narratives
│   │       ├── phase6_outcome.py         # "What if I ignore?" messaging
│   │       ├── phase7_action.py          # Actionable recommendations
│   │       ├── phase8_caregiver.py       # Family/caregiver escalation
│   │       ├── phase9_language.py        # Multilingual formatting
│   │       └── pipeline.py              # Orchestrator (runs Phase 1→9)
│   │
│   └── venv/                             # Python virtual environment
│
├── frontend/                             # React Application
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── index.html
│   │
│   ├── public/
│   │   └── favicon.ico
│   │
│   └── src/
│       ├── main.tsx                      # App entry point
│       ├── App.tsx                       # Root component + routing
│       ├── index.css                     # Tailwind imports + global styles
│       │
│       ├── api/
│       │   └── triageApi.ts              # Axios client for /triage endpoint
│       │
│       ├── components/
│       │   ├── Layout/
│       │   │   ├── Navbar.tsx            # Top nav with language toggle + dark mode
│       │   │   └── Footer.tsx
│       │   ├── SymptomForm/
│       │   │   ├── SymptomForm.tsx       # Main form (age, gender, symptom chips)
│       │   │   ├── SymptomChip.tsx       # Individual symptom tag
│       │   │   └── VoiceInput.tsx        # Web Speech API mic button
│       │   ├── Dashboard/
│       │   │   ├── RiskCard.tsx          # Risk level with color-coded indicator
│       │   │   ├── ExplanationPanel.tsx  # "What we noticed / Why it matters"
│       │   │   ├── OutcomePanel.tsx      # "What if I ignore this?"
│       │   │   ├── ActionPanel.tsx       # Recommended actions
│       │   │   └── CaregiverAlert.tsx    # Caregiver notification suggestion
│       │   └── History/
│       │       └── HistoryList.tsx       # Past triage records (localStorage)
│       │
│       ├── context/
│       │   ├── ThemeContext.tsx           # Dark/light mode state
│       │   └── LanguageContext.tsx        # i18n language state
│       │
│       ├── hooks/
│       │   ├── useTriage.ts              # Custom hook for triage API call
│       │   ├── useVoice.ts               # Web Speech API hook
│       │   └── useHistory.ts             # localStorage history hook
│       │
│       ├── i18n/
│       │   ├── en.json                   # English strings
│       │   ├── hi.json                   # Hindi strings
│       │   └── mr.json                   # Marathi strings
│       │
│       ├── types/
│       │   └── index.ts                  # TypeScript interfaces
│       │
│       └── utils/
│           └── constants.ts              # Symptom list, risk colors, etc.
```

---

## 🔬 ML Model Integration (Naive Bayes)

### Dataset Format (from screenshot)
| Column A | Column B | Column C | ... | Column T |
|----------|----------|----------|-----|----------|
| Disease  | symptom1 | symptom2 | ... | symptomN |

- **Algorithm:** Gaussian / Multinomial Naive Bayes
- **Input:** Binary vector (132 symptom columns → 1 if present, 0 if absent)
- **Output:** Predicted disease name + probability scores

### ML Files
| File | Purpose |
|------|---------|
| `ml/train_model.py` | Reads CSV, encodes, trains NB, saves .pkl files |
| `ml/predictor.py` | Loads .pkl, accepts symptom list, returns prediction |
| `ml/model.pkl` | Serialized trained model |
| `ml/label_encoder.pkl` | Maps disease indices ↔ disease names |
| `ml/symptom_columns.pkl` | Ordered list of all symptom feature names |

### How ML Integrates with Phase 4
```
Phase 1 (input) → normalized symptoms
                        │
                        ▼
Phase 4 (risk) ─── ML Predictor ──→ predicted_disease + confidence
                │                         │
                │   Rule Engine ──────────┘
                │   (clusters + silent     
                │    emergency patterns)   
                ▼
         Final risk_level + confidence_band
```

- ML prediction **supplements** rule-based risk (does not replace it)
- If ML confidence > 70% AND disease is severe → escalate risk level
- If ML confidence < 50% → rely purely on rule-based assessment

---

## 🔌 API Contract

### `GET /` — Health Check
```json
{ "status": "Avalon backend running", "version": "1.0.0" }
```

### `POST /triage` — Main Triage Endpoint

**Request:**
```json
{
  "age": 55,
  "gender": "male",
  "symptoms": ["chest_pain", "breathing_difficulty", "fatigue"],
  "raw_text": "I have just a little chest pain and some breathlessness",
  "input_method": "voice",
  "language": "en"
}
```

**Response:**
```json
{
  "risk_level": "High",
  "confidence_band": "high",
  "predicted_condition": "Possible cardiac-related concern",
  "ml_confidence": 0.82,
  "explanation": {
    "what_we_noticed": "You reported chest pain and breathing difficulty...",
    "why_it_matters": "This combination can sometimes be associated with...",
    "what_this_means": "Based on the pattern, we recommend..."
  },
  "neglect_detected": "Yes",
  "neglect_reason": "You used the word 'just' when describing chest pain...",
  "silent_emergency_flag": "High",
  "risk_pattern_explanation": "Chest pain in individuals above 40...",
  "what_if_ignored": {
    "short_term": "In some cases, delaying care can lead to...",
    "long_term": "Over time, untreated symptoms may..."
  },
  "recommended_action": "Please seek immediate medical attention...",
  "caregiver_alert_suggestion": "Yes",
  "caregiver_reason": "Given the high risk level, involving a trusted person...",
  "language": "en",
  "disclaimer": "This is not a medical diagnosis. Please consult a healthcare professional."
}
```

### `GET /symptoms` — Get All Available Symptoms
```json
{
  "symptoms": ["chest_pain", "fever", "cough", "headache", ...],
  "categories": {
    "cardiac": ["chest_pain", "palpitations"],
    "respiratory": ["cough", "breathing_difficulty"],
    ...
  }
}
```

### `GET /history` — (Optional) If server-side history is needed

---

## 🎨 Frontend Design Spec

### Pages / Views
| Route | Component | Description |
|-------|-----------|-------------|
| `/` | `SymptomForm` | Main input – select symptoms, enter age/gender |
| `/result` | `Dashboard` | Risk card + explanation + actions |
| `/history` | `HistoryList` | Past triage records |

### UI Features
| Feature | Implementation |
|---------|---------------|
| **Symptom Selection** | Searchable multi-select chips (grouped by category) |
| **Risk Dashboard** | Color-coded card (Green/Yellow/Red) + animated gauge |
| **Voice Input** | Web Speech API → mic button on form |
| **Dark Mode** | Tailwind `dark:` classes + context toggle |
| **Multilingual** | JSON i18n files + `LanguageContext` |
| **History** | `localStorage` with timestamp + risk summary |

### Color Scheme
| Risk Level | Color | Tailwind Class |
|------------|-------|----------------|
| Low | Green | `bg-green-500` |
| Medium | Amber | `bg-amber-500` |
| High | Red | `bg-red-500` |

---

## 🛡️ Ethical Guardrails (Always Active)

- ❌ No diagnosis — only "possible conditions" with disclaimers
- ❌ No treatment plans or medication advice
- ❌ No absolute statements ("you have X")
- ✅ Every response includes disclaimer
- ✅ Encourage professional care when needed
- ✅ Calm, empathetic, non-alarming tone
- ✅ Respect user autonomy

---

## 🚀 Implementation Order

### Phase A: Backend Core (7 files)
1. `ml/train_model.py` – Train & serialize Naive Bayes
2. `ml/predictor.py` – Load model & predict
3. `engine/phase1_input.py` – Parse & normalize
4. `engine/phase2_neglect.py` – Neglect detection
5. `engine/phase3_silent.py` – Silent emergency detection
6. `engine/phase4_risk.py` – Risk classification (ML + rules)
7. `engine/phase5_explain.py` – Explainability

### Phase B: Backend Complete (5 files)
8. `engine/phase6_outcome.py` – Outcome awareness
9. `engine/phase7_action.py` – Recommendations
10. `engine/phase8_caregiver.py` – Caregiver logic
11. `engine/phase9_language.py` – Multilingual
12. `engine/pipeline.py` – Wire all phases

### Phase C: Backend API (3 files)
13. `routes.py` – All endpoints
14. `run.py` – Entry point
15. `requirements.txt` – Final deps

### Phase D: React Frontend (scaffold)
16. Vite + TS + Tailwind project setup
17. API service layer
18. Symptom form + voice input
19. Risk dashboard + panels
20. History, dark mode, i18n

---

## 📦 Dependencies

### Backend (`requirements.txt`)
```
Flask==3.1.2
flask-cors==6.0.2
scikit-learn>=1.3.0
pandas>=2.0.0
joblib>=1.3.0
numpy>=1.24.0
```

### Frontend (`package.json`)
```
react, react-dom, react-router-dom
typescript, vite, @vitejs/plugin-react
tailwindcss, postcss, autoprefixer
axios
framer-motion
react-icons
```

---

*This plan maps directly to project Features 0–7, integrates the Naive Bayes ML model,  
and defines a complete React frontend — all safe for healthcare-domain use.*
