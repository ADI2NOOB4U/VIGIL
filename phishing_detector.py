import pandas as pd
import requests
import pickle
import os
from urllib.parse import urlparse
from feature_extractor import extract_features

MODEL_URL = "https://drive.google.com/uc?id=1bqVkYbeC-tM_LEQOwZ2ufAuB29QOxdNU"
FEATURE_URL = "https://drive.google.com/uc?id=1MZsRELGflCX95pDBawHx77vH20Z1Aein"

def download_file(url, filename):
    if not os.path.exists(filename):
        r = requests.get(url)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
        else:
            raise Exception(f"Failed to download {filename}")

# Download once
download_file(MODEL_URL, "phishing_model.pkl")
download_file(FEATURE_URL, "feature_names.pkl")

# Load model + features
with open("phishing_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)


def check_phishing(url: str):
    # 🔹 Trusted domains (whitelist)
    trusted_domains = [
        "github.com",
        "amazon.com",
        "amazon.in",
        "google.com",
        "microsoft.com",
        "apple.com",
        "linkedin.com"
    ]

    # 🔹 Extract domain safely
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # 🔥 Secure whitelist check
    if any(domain == d or domain.endswith("." + d) for d in trusted_domains):
        return {
            "result": "SAFE",
            "confidence": 0.99,
            "features": {}
        }

    try:
        # 🔹 Feature extraction
        features = extract_features(url)

        # 🔹 Convert to DataFrame
        df = pd.DataFrame([features])

        # 🔥 Add missing features
        for feature in feature_names:
            if feature not in df.columns:
                df[feature] = 0

        # 🔹 Correct feature order
        df = df[feature_names]

        # 🔹 Prediction
        prediction = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]

        # 🔥 Improved thresholds
        if prob > 0.85:
            result = "PHISHING"
        elif prob > 0.60:
            result = "SUSPICIOUS"
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