import pandas as pd
import pickle
from feature_extractor import extract_features

# Load model + feature names
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