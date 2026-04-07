import pandas as pd
import numpy as np
import pickle
from feature_extractor import extract_features

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("🚀 Loading dataset...")

# Load dataset
df = pd.read_csv("final_dataset_v2.csv")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Basic cleaning
df = df[['url', 'label']].dropna()
df = df.drop_duplicates()

print(f"📊 Total samples: {len(df)}")
print("\n📊 Label distribution:")
print(df['label'].value_counts())

# =========================
# FEATURE EXTRACTION
# =========================
print("⚙️ Extracting features... (this may take time)")

features = df['url'].apply(lambda x: extract_features(x))
X = pd.DataFrame(features.tolist())

y = df['label']

print(f"✅ Features shape: {X.shape}")

# =========================
# SAVE FEATURE NAMES
# =========================
feature_names = X.columns.tolist()
pickle.dump(feature_names, open("feature_names.pkl", "wb"))

# =========================
# TRAIN / TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("📊 Train size:", len(X_train))
print("📊 Test size:", len(X_test))

# =========================
# MODEL (MAXED RF)
# =========================
print("🧠 Training model...")

model = RandomForestClassifier(
    n_estimators=400,       # more trees
    max_depth=None,         # allow full depth
    min_samples_split=5,    # reduce overfitting
    min_samples_leaf=2,     # smoother decisions
    n_jobs=-1,
    random_state=42
)
model.fit(X_train, y_train)

# =========================
# EVALUATION
# =========================
print("📈 Evaluating model...")

y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)

print("\n🔥 ACCURACY:", acc)

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

print("\n📉 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# =========================
# FEATURE IMPORTANCE (🔥 DEMO GOLD)
# =========================
importances = model.feature_importances_
feat_imp = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print("\n🔥 Top 10 Important Features:")
print(feat_imp.head(10))

# Save feature importance
feat_imp.to_csv("feature_importance.csv", index=False)

# =========================
# SAVE MODEL
# =========================
pickle.dump(model, open("phishing_model.pkl", "wb"))

print("\n✅ MODEL SAVED SUCCESSFULLY")