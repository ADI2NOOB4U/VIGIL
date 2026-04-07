import pandas as pd
import pickle
from feature_extractor import extract_features

# Load model + feature names
import requests
import pickle
import os

MODEL_URL = "YOUR_MODEL_LINK"
FEATURE_URL = "YOUR_FEATURE_LINK"

def download_file(url, filename):
    if not os.path.exists(filename):
        r = requests.get(url)
        with open(filename, "wb") as f:
            f.write(r.content)

# Download once
download_file(MODEL_URL, "phishing_model.pkl")
download_file(FEATURE_URL, "feature_names.pkl")

# Load
model = pickle.load(open("phishing_model.pkl", "rb"))
feature_names = pickle.load(open("feature_names.pkl", "rb"))

def check_phishing(url: str):
    try:
        # 🔹 Extract features from URL
        features = extract_features(url)

        # 🔹 Convert to DataFrame
        df = pd.DataFrame([features])

        # 🔥 Add missing features (if any)
        for feature in feature_names:
            if feature not in df.columns:
                df[feature] = 0

        # 🔹 Ensure correct order
        df = df[feature_names]

        # 🔹 Prediction
        prediction = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]

        # 🔹 Output labels with confidence threshold
        if prob > 0.7:
            result = "PHISHING"
        elif prob > 0.4:
            result = " SUSPICIOUS"
        else:
            result = "SAFE"

        return {
            "result": result,
            "confidence": round(prob, 4),
            "features": features
        }

    except Exception as e:
        return {
            "result": "ERROR",
            "confidence": 0,
            "error": str(e)
        }