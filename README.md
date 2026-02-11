 🏥 AI-Powered Health Symptom Triage and Risk Assessment System

 Explainable • Voice-Enabled • Multilingual • Ethical AI

> *Tagline:* When symptoms are unclear, clarity saves lives.

---

 📌 Overview

The *AI-Powered Health Symptom Triage and Risk Assessment System* is a web-based application that helps users understand the urgency of their health symptoms and avoid dangerous delays in medical care.

Unlike traditional symptom checkers that passively list possible conditions, this system actively detects *hidden medical risk, explains **why urgency exists, highlights the **consequences of inaction, and **escalates care ethically* when necessary.

To ensure inclusivity and real-world usability, the system supports *voice-based symptom input* and *multilingual access (English, Hindi, Marathi)*, making it accessible to non-English speakers, elderly users, and individuals with limited literacy or physical disabilities.

⚠️ This tool provides *decision support only* and does *not* offer medical diagnosis.

---

 ❓ The Problem It Solves

Many people:

* Underestimate or downplay symptoms (symptom neglect)
* Misjudge urgency due to fear, denial, or lack of medical knowledge
* Delay seeking care for conditions that initially feel mild
* Cannot use English-only, text-based health tools

This leads to *preventable medical emergencies, especially in cases of **silent or atypical presentations* (e.g., heart attacks without chest pain).

Existing symptom checkers:

* Assume accurate self-reporting
* Rely on static symptom inputs
* Provide risk scores without explanation
* Exclude non-English speakers and low-literacy users

---

 💡 What This System Does

Users can:

* Enter or *speak* their symptoms naturally
* Use the interface in *English, Hindi, or Marathi*
* Receive a *Low / Medium / High* risk assessment
* Understand why that risk was assigned
* Learn what may happen if symptoms are ignored
* Alert a trusted family member in high-risk cases

---

 ⭐ Key Features

 1️⃣ Symptom Neglect Detection

Identifies mismatches between user-reported severity and statistically high-risk symptom patterns.

 2️⃣ Silent Emergency Detection

Flags atypical or low-symptom presentations of serious conditions using population-level data patterns.

 3️⃣ Explainability-First Risk Narratives

Provides clear, human-readable explanations instead of opaque scores.

 4️⃣ “What If I Ignore This?” Outcome Awareness

Ethically communicates the possible consequences of delaying care.

 6️⃣ 🎤 Voice-Based Symptom Input

* Speak symptoms naturally instead of typing
* Uses *Web Speech API*
* Real-time transcription with visual listening indicator
* Automatically triggers AI analysis after speech ends

 7️⃣ 🌐 Multilingual Access

* Full UI support for *English, Hindi, Marathi*
* Voice recognition adapts to selected language
* Built-in frontend internationalization (i18n)

---

 🧠 Why This Is AI

* Uses *machine learning models* trained on healthcare datasets
* Learns symptom–risk correlations instead of fixed rules
* Handles uncertainty and atypical cases
* Provides explainable, probabilistic outcomes

> Machine Learning is a core subfield of Artificial Intelligence — this system is *AI by design*.

---

 🏗️ System Architecture

 Frontend (frontend/)

* index.html – Responsive SPA with Bootstrap 5, Three.js (3D model), voice input, and language switcher
* script_modern.js – App logic (i18n, Web Speech API, symptom handling, API calls, visualization)
* style_modern.css – Modern medical UI styling
* exports/ – Generated assessment reports

 Backend (backend/)

* run.py – Flask REST API (/predict, /symptoms, /analytics, etc.)
* utils.py – Input preprocessing, NLP negation handling, risk mapping
* config.py – Centralized configuration
* model_loader.py – ML model loading & inference
* serve_keras_model.py – Optional TensorFlow/Keras serving
* generate_report_from_json.py – Report generation

 ML Training (ml_training/)

* health_symptom_model.ipynb – Training & evaluation
* train_and_export.py – Model training script
* dataset/ – Training data

 Models (ml_model/)

* model.pkl – Trained ML classifier
* label_encoder.pkl – Risk level encoder
* vectorizer.pkl – TF-IDF / NLP vectorizer

---

 🧰 Technology Stack

| Layer                     | Category                    | Technology / Tools                                                                                                                                                                               |
| ------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Frontend**              | Framework                   | React (Functional Components)                                                                                                                                                                    |
|                           | Language                    | TypeScript                                                                                                                                                                                       |
|                           | Build Tool / Bundler        | Vite                                                                                                                                                                                             |
|                           | Styling                     | Tailwind CSS, PostCSS                                                                                                                                                                            |
|                           | State Management            | React Context API                                                                                                                                                                                |
|                           | Internationalization (i18n) | JSON-based translations (English, Hindi, Marathi)                                                                                                                                                |
|                           | Voice Input                 | Web Speech API (SpeechRecognition / webkitSpeechRecognition)                                                                                                                                     |
|                           | API Communication           | Custom API Service Layer (REST using Fetch / Axios)                                                                                                                                              |
| **Backend**               | Programming Language        | Python 3.13 / 3.14                                                                                                                                                                               |
|                           | Web Framework               | Flask                                                                                                                                                                                            |
|                           | API Architecture            | RESTful APIs                                                                                                                                                                                     |
|                           | CORS Handling               | Flask-CORS                                                                                                                                                                                       |
| **Machine Learning & AI** | ML Framework                | scikit-learn                                                                                                                                                                                     |
|                           | Model Type                  | Supervised Classification Model                                                                                                                                                                  |
|                           | NLP Vectorization           | TF-IDF Vectorizer                                                                                                                                                                                |
|                           | Label Encoding              | scikit-learn LabelEncoder                                                                                                                                                                        |
|                           | Model Serialization         | Pickle / joblib (`.pkl` files)                                                                                                                                                                   |
| **AI Decision Engine**    | Architecture                | Phase-wise Explainable AI Pipeline                                                                                                                                                               |
|                           | Pipeline Phases             | Input Parsing, Symptom Neglect Detection, Silent Emergency Detection, Risk Classification, Explainability, Outcome Awareness, Action Recommendation, Caregiver Escalation, Multilingual Handling |
| **Data & Knowledge Base** | Medical Data                | CSV-based Symptom, Severity, Description & Precaution Datasets                                                                                                                                   |
|                           | Knowledge System            | Rule-based + Data-driven Hybrid                                                                                                                                                                  |
| **Testing**               | Backend Testing             | Python Unit Tests                                                                                                                                                                                |
|                           | NLP & i18n Testing          | Translation & Phrase Mapping Tests                                                                                                                                                               |
| **Runtime & Tooling**     | JavaScript Runtime          | Node.js                                                                                                                                                                                          |
|                           | Package Manager             | npm                                                                                                                                                                                              |
|                           | Version Control             | Git                                                                                                                                                                                              |


---

 🚀 How to Run the Project

bash
 1. Clone the repository
git clone https://github.com/Ritikmehta080905/Healthcare.git
cd Healthcare

 2. Install backend dependencies
cd backend
pip install -r requirements.txt

 3. Start the backend server
python run.py
 Server runs at http://localhost:5000

 4. Open the frontend
 Open frontend/index.html in Chrome or Edge (recommended for voice support)

 OR use the unified launcher
cd ..
python start.py


---

 🌍 Impact & Significance

* Reduces dangerous delays caused by symptom neglect
* Detects silent and atypical emergencies
* Makes AI healthcare tools accessible to *non-English speakers*
* Removes literacy and typing barriers with *voice input*
* Promotes ethical, explainable, and inclusive AI

This project demonstrates how AI can go beyond prediction to *change outcomes and democratize healthcare access*.

---

## ⚠️ Disclaimer

> This application is for *educational and informational purposes only*.
> It does *not* provide medical diagnosis or treatment.
> Always consult a qualified healthcare professional for medical decisions.

---
