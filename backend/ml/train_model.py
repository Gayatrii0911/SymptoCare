"""
ML Model Training Pipeline for Health Triage Copilot
=====================================================
Trains multiple classifiers on the disease-symptom dataset,
evaluates accuracy / precision / recall / F1, and saves the best model.

Dataset:
  - dataset.csv:             Disease → Symptom_1..Symptom_17
  - Symptom-severity.csv:    Symptom → weight (1-7)
  - symptom_Description.csv: Disease → textual description
  - symptom_precaution.csv:  Disease → 4 precautions

Output files (saved to ml/ directory):
  - model.pkl             – best trained classifier
  - label_encoder.pkl     – LabelEncoder for disease names
  - symptom_columns.pkl   – ordered list of all 131 symptom feature names
  - severity_map.pkl      – symptom → severity weight mapping
  - disease_info.pkl      – disease → {description, precautions, severity_tier}
  - training_report.txt   – full evaluation metrics
"""

import os
import sys
import pickle
import warnings

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

warnings.filterwarnings("ignore")

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = BASE_DIR  # CSVs are in backend/
ML_DIR = os.path.join(BASE_DIR, "ml")
os.makedirs(ML_DIR, exist_ok=True)


# ── Disease severity tiers (for triage risk mapping) ─────────────────────────
HIGH_SEVERITY_DISEASES = {
    "Heart attack", "Paralysis (brain hemorrhage)", "AIDS",
    "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E",
    "hepatitis A", "Tuberculosis", "Pneumonia", "Dengue",
    "Malaria", "Typhoid", "Hypoglycemia",
}

MEDIUM_SEVERITY_DISEASES = {
    "Diabetes", "Hypertension", "Hyperthyroidism", "Hypothyroidism",
    "Jaundice", "Alcoholic hepatitis", "Chronic cholestasis",
    "Gastroenteritis", "Peptic ulcer diseae", "Urinary tract infection",
    "Dimorphic hemmorhoids(piles)", "Bronchial Asthma",
    "(vertigo) Paroymsal  Positional Vertigo",
}

# Everything else → Low severity


def load_datasets():
    """Load and return all 4 CSVs."""
    df = pd.read_csv(os.path.join(DATA_DIR, "dataset.csv"))
    severity = pd.read_csv(os.path.join(DATA_DIR, "Symptom-severity.csv"))
    descriptions = pd.read_csv(os.path.join(DATA_DIR, "symptom_Description.csv"))
    precautions = pd.read_csv(os.path.join(DATA_DIR, "symptom_precaution.csv"))
    return df, severity, descriptions, precautions


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from disease and symptom columns."""
    df["Disease"] = df["Disease"].str.strip()
    symptom_cols = [c for c in df.columns if c.startswith("Symptom")]
    for col in symptom_cols:
        df[col] = df[col].astype(str).str.strip().replace({"nan": "", "": ""})
    return df


def build_binary_features(df: pd.DataFrame):
    """
    Convert the multi-column symptom format into a binary feature matrix.
    Each unique symptom becomes a column (1 = present, 0 = absent).
    Returns: (feature_df, symptom_columns_sorted)
    """
    symptom_cols = [c for c in df.columns if c.startswith("Symptom")]

    # Collect all unique symptoms
    all_symptoms = set()
    for col in symptom_cols:
        vals = df[col].dropna().str.strip().unique()
        all_symptoms.update(v for v in vals if v and v != "nan")
    all_symptoms.discard("")

    symptom_list = sorted(all_symptoms)
    print(f"  Total unique symptoms: {len(symptom_list)}")

    # Build binary matrix
    binary_data = np.zeros((len(df), len(symptom_list)), dtype=int)
    symptom_index = {s: i for i, s in enumerate(symptom_list)}

    for _, row in df.iterrows():
        for col in symptom_cols:
            symptom = str(row[col]).strip()
            if symptom and symptom != "nan" and symptom in symptom_index:
                binary_data[row.name, symptom_index[symptom]] = 1

    feature_df = pd.DataFrame(binary_data, columns=symptom_list)
    return feature_df, symptom_list


def build_severity_map(severity_df: pd.DataFrame) -> dict:
    """Build symptom → weight mapping."""
    severity_df["Symptom"] = severity_df["Symptom"].str.strip().str.lower()
    return dict(zip(severity_df["Symptom"], severity_df["weight"]))


def build_disease_info(descriptions_df, precautions_df) -> dict:
    """Build disease → {description, precautions, severity_tier} mapping."""
    info = {}

    for _, row in descriptions_df.iterrows():
        disease = str(row["Disease"]).strip()
        info[disease] = {
            "description": str(row["Description"]).strip(),
            "precautions": [],
            "severity_tier": "Low",
        }

    for _, row in precautions_df.iterrows():
        disease = str(row["Disease"]).strip()
        if disease not in info:
            info[disease] = {"description": "", "precautions": [], "severity_tier": "Low"}
        precs = []
        for col in ["Precaution_1", "Precaution_2", "Precaution_3", "Precaution_4"]:
            val = str(row.get(col, "")).strip()
            if val and val != "nan":
                precs.append(val)
        info[disease]["precautions"] = precs

    # Assign severity tiers
    for disease in info:
        if disease in HIGH_SEVERITY_DISEASES:
            info[disease]["severity_tier"] = "High"
        elif disease in MEDIUM_SEVERITY_DISEASES:
            info[disease]["severity_tier"] = "Medium"
        else:
            info[disease]["severity_tier"] = "Low"

    return info


def train_and_evaluate(X_train, X_test, y_train, y_test, le: LabelEncoder):
    """Train multiple models, evaluate, and return the best one."""

    models = {
        "MultinomialNB": MultinomialNB(),
        "BernoulliNB": BernoulliNB(),
        "GaussianNB": GaussianNB(),
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "SVM": SVC(kernel="rbf", probability=True, random_state=42),
    }

    results = {}
    report_lines = []

    report_lines.append("=" * 70)
    report_lines.append("  HEALTH TRIAGE COPILOT – MODEL TRAINING REPORT")
    report_lines.append("=" * 70)
    report_lines.append(f"  Training samples: {len(X_train)}")
    report_lines.append(f"  Testing samples:  {len(X_test)}")
    report_lines.append(f"  Features:         {X_train.shape[1]} symptoms")
    report_lines.append(f"  Classes:          {len(le.classes_)} diseases")
    report_lines.append("=" * 70)
    report_lines.append("")

    best_model_name = None
    best_accuracy = 0
    best_model = None

    for name, model in models.items():
        print(f"\n  Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        # Cross-validation (5-fold)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy")

        results[name] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
        }

        print(f"    Accuracy:  {acc:.4f}")
        print(f"    Precision: {prec:.4f}")
        print(f"    Recall:    {rec:.4f}")
        print(f"    F1 Score:  {f1:.4f}")
        print(f"    CV Mean:   {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

        report_lines.append(f"── {name} {'─' * (50 - len(name))}")
        report_lines.append(f"  Accuracy:        {acc:.4f}  ({acc*100:.1f}%)")
        report_lines.append(f"  Precision (wtd): {prec:.4f}")
        report_lines.append(f"  Recall (wtd):    {rec:.4f}")
        report_lines.append(f"  F1 Score (wtd):  {f1:.4f}")
        report_lines.append(f"  5-Fold CV:       {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        report_lines.append("")

        if acc > best_accuracy:
            best_accuracy = acc
            best_model_name = name
            best_model = model

    # ── Best model detailed report ───────────────────────────────────────
    report_lines.append("=" * 70)
    report_lines.append(f"  ★ BEST MODEL: {best_model_name}")
    report_lines.append(f"  ★ ACCURACY:   {best_accuracy:.4f}  ({best_accuracy*100:.1f}%)")
    report_lines.append("=" * 70)
    report_lines.append("")

    # Detailed classification report for the best model
    y_pred_best = best_model.predict(X_test)
    cls_report = classification_report(
        y_test, y_pred_best,
        target_names=le.classes_,
        zero_division=0,
    )
    report_lines.append("DETAILED CLASSIFICATION REPORT (Best Model):")
    report_lines.append(cls_report)

    # Comparison table
    report_lines.append("\n── MODEL COMPARISON TABLE ──────────────────────────")
    report_lines.append(f"{'Model':<22} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10} {'CV Mean':>10}")
    report_lines.append("-" * 74)
    for name, r in sorted(results.items(), key=lambda x: x[1]["accuracy"], reverse=True):
        marker = " ★" if name == best_model_name else ""
        report_lines.append(
            f"{name:<22} {r['accuracy']:>9.4f} {r['precision']:>10.4f} "
            f"{r['recall']:>10.4f} {r['f1']:>10.4f} {r['cv_mean']:>10.4f}{marker}"
        )

    return best_model, best_model_name, results, "\n".join(report_lines)


def main():
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║   Health Triage Copilot – ML Training Pipeline       ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    # 1. Load data
    print("📂 Loading datasets...")
    df, severity_df, descriptions_df, precautions_df = load_datasets()
    print(f"  Dataset shape: {df.shape}")

    # 2. Clean
    print("\n🧹 Cleaning data...")
    df = clean_dataset(df)

    # 3. Build binary features
    print("\n🔧 Building binary symptom features...")
    X_features, symptom_columns = build_binary_features(df)

    # 4. Encode labels
    print("\n🏷️  Encoding disease labels...")
    le = LabelEncoder()
    y = le.fit_transform(df["Disease"])
    print(f"  Classes: {len(le.classes_)} diseases")

    # 5. Build auxiliary data
    print("\n📊 Building severity map & disease info...")
    severity_map = build_severity_map(severity_df)
    disease_info = build_disease_info(descriptions_df, precautions_df)
    print(f"  Severity entries: {len(severity_map)}")
    print(f"  Disease info entries: {len(disease_info)}")

    # 6. Train/test split
    print("\n✂️  Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_features.values, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")

    # 7. Train & evaluate all models
    print("\n🤖 Training & evaluating models...")
    best_model, best_name, results, report = train_and_evaluate(
        X_train, X_test, y_train, y_test, le
    )

    # 8. Save artifacts
    print(f"\n💾 Saving best model ({best_name}) and artifacts to ml/...")

    with open(os.path.join(ML_DIR, "model.pkl"), "wb") as f:
        pickle.dump(best_model, f)

    with open(os.path.join(ML_DIR, "label_encoder.pkl"), "wb") as f:
        pickle.dump(le, f)

    with open(os.path.join(ML_DIR, "symptom_columns.pkl"), "wb") as f:
        pickle.dump(symptom_columns, f)

    with open(os.path.join(ML_DIR, "severity_map.pkl"), "wb") as f:
        pickle.dump(severity_map, f)

    with open(os.path.join(ML_DIR, "disease_info.pkl"), "wb") as f:
        pickle.dump(disease_info, f)

    # Save training report
    report_path = os.path.join(ML_DIR, "training_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"  ✅ model.pkl")
    print(f"  ✅ label_encoder.pkl")
    print(f"  ✅ symptom_columns.pkl")
    print(f"  ✅ severity_map.pkl")
    print(f"  ✅ disease_info.pkl")
    print(f"  ✅ training_report.txt")

    # 9. Print report
    print("\n" + report)

    print("\n✅ Training complete! All artifacts saved to ml/ directory.\n")


if __name__ == "__main__":
    main()
