import pandas as pd
import requests
import pickle
import os
from urllib.parse import urlparse
from feature_extractor import extract_features

# =========================
# 🔗 MODEL DOWNLOAD LINKS
# =========================
MODEL_URL = "https://drive.google.com/uc?id=1bqVkYbeC-tM_LEQOwZ2ufAuB29QOxdNU"
FEATURE_URL = "https://drive.google.com/uc?id=1MZsRELGflCX95pDBawHx77vH20Z1Aein"


def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        r = requests.get(url)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
        else:
            raise Exception(f"Failed to download {filename}")


# =========================
# 📥 DOWNLOAD MODEL FILES
# =========================
download_file(MODEL_URL, "phishing_model.pkl")
download_file(FEATURE_URL, "feature_names.pkl")


# =========================
# 🧠 LOAD MODEL + FEATURES
# =========================
with open("phishing_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)


# =========================
# 🚀 MAIN FUNCTION
# =========================
def check_phishing(url: str):

    # 🔹 Normalize URL
    if not url.startswith("http"):
        url = "http://" + url

    # 🔹 Trusted domains (whitelist)
    trusted_domains = [
        "github.com",
        "amazon.com",
        "amazon.in",
        "google.com",
        "microsoft.com",
        "apple.com",
        "linkedin.com",
        "youtube.com",
        "facebook.com"
    ]

    # 🔹 Extract domain
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # 🔥 Clean domain (remove www)
    if domain.startswith("www."):
        domain = domain[4:]

    # 🔥 Whitelist check (SAFE override)
    if any(domain == d or domain.endswith("." + d) for d in trusted_domains):
        return {
            "result": "SAFE",
            "confidence": 0.99,
            "features": {}
        }

    try:
        # =========================
        # 🔍 FEATURE EXTRACTION
        # =========================
        features = extract_features(url)

        if not isinstance(features, dict):
            raise Exception("Feature extractor must return a dictionary")

        # =========================
        # 📊 DATAFRAME BUILD
        # =========================
        df = pd.DataFrame([features])

        # Add missing features
        for feature in feature_names:
            if feature not in df.columns:
                df[feature] = 0

        # Ensure correct order
        df = df[feature_names]

        # =========================
        # 🧪 DEBUG BLOCK
        # =========================
        print("\n========== DEBUG ==========")
        print("URL:", url)
        print("Domain:", domain)
        print("Classes:", model.classes_)

        prediction = model.predict(df)[0]
        probs = model.predict_proba(df)[0]

        print("Prediction:", prediction)
        print("Probabilities:", probs)
        print("Feature Sample:", df.iloc[0].to_dict())
        print("===========================\n")

        # =========================
        # 🧠 SMART PROBABILITY FIX
        # =========================
        classes = list(model.classes_)

        if 1 in classes:
            phishing_index = classes.index(1)
        else:
            # fallback safety
            phishing_index = len(probs) - 1

        prob = float(probs[phishing_index])

        # =========================
        # 🎯 DECISION LOGIC
        # =========================
        if prob > 0.90:
            result = "PHISHING"
        elif prob > 0.65:
            result = "SUSPICIOUS"
        else:
            result = "SAFE"

        return {
            "result": result,
            "confidence": round(prob, 4),
            "features": features
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {
            "result": "ERROR",
            "confidence": 0,
            "error": str(e)
        }