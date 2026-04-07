from urllib.parse import urlparse
import re
import math


# =========================
# 🔢 ENTROPY FUNCTION
# =========================
def shannon_entropy(s):
    if not s:
        return 0
    prob = [float(s.count(c)) / len(s) for c in set(s)]
    return -sum([p * math.log2(p) for p in prob if p > 0])


# =========================
# 🚀 MAIN FEATURE FUNCTION
# =========================
def extract_features(url):
    features = {}

    # 🔹 Normalize URL
    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path

    # 🔥 Clean domain
    if domain.startswith("www."):
        domain = domain[4:]

    # =========================
    # 📏 BASIC FEATURES
    # =========================
    features["URLLength"] = len(url)
    features["DomainLength"] = len(domain)

    # =========================
    # 🌐 IP ADDRESS CHECK (FIXED)
    # =========================
    features["IsDomainIP"] = 1 if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", domain) else 0

    # =========================
    # 🔒 HTTPS
    # =========================
    features["IsHTTPS"] = 1 if parsed.scheme == "https" else 0

    # =========================
    # 🌍 SUBDOMAINS (FIXED)
    # =========================
    features["NoOfSubDomain"] = max(domain.count(".") - 1, 0)

    # =========================
    # 🔐 OBFUSCATION
    # =========================
    features["HasObfuscation"] = 1 if "%" in url or "@" in url else 0

    # =========================
    # 🔣 SPECIAL CHARACTERS
    # =========================
    features["NoOfEqualsInURL"] = url.count("=")
    features["NoOfQMarkInURL"] = url.count("?")
    features["NoOfAmpersandInURL"] = url.count("&")
    features["NoOfAtInURL"] = url.count("@")
    features["NoOfHyphenInURL"] = url.count("-")

    # =========================
    # 🔢 DIGITS
    # =========================
    digits = sum(c.isdigit() for c in url)
    features["NoOfDigitsInURL"] = digits
    features["DigitRatioInURL"] = digits / len(url) if len(url) > 0 else 0

    # =========================
    # 🔤 LETTERS
    # =========================
    letters = sum(c.isalpha() for c in url)
    features["NoOfLettersInURL"] = letters
    features["LetterRatioInURL"] = letters / len(url) if len(url) > 0 else 0

    # =========================
    # 🚨 SUSPICIOUS KEYWORDS (IMPROVED)
    # =========================
    suspicious_words = [
        "login", "verify", "update", "bank", "secure",
        "account", "free", "bonus", "signin", "confirm",
        "password", "wallet", "crypto", "pay"
    ]

    features["HasSuspiciousWord"] = int(
        any(word in url.lower() for word in suspicious_words)
    )

    # =========================
    # 🌐 SUSPICIOUS TLD
    # =========================
    suspicious_tlds = [".tk", ".ml", ".ga", ".cf", ".xyz", ".top"]
    features["HasSuspiciousTLD"] = int(
        any(domain.endswith(tld) for tld in suspicious_tlds)
    )

    # =========================
    # 📂 PATH LENGTH
    # =========================
    features["PathLength"] = len(path)

    # =========================
    # 🎲 ENTROPY (FIXED SAFE)
    # =========================
    features["URLEntropy"] = shannon_entropy(url)

    # =========================
    # 🏷️ BRAND MISUSE DETECTION (FIXED)
    # =========================
    trusted_brands = ["amazon", "google", "github", "facebook", "microsoft", "apple"]

    # brand in domain but not exact match → suspicious
    features["HasTrustedBrand"] = int(
        any(brand in domain and not domain.endswith(brand + ".com") for brand in trusted_brands)
    )

    # =========================
    # 🌍 TRUSTED TLD
    # =========================
    trusted_tlds = [".com", ".org", ".net", ".edu", ".gov"]
    features["IsTrustedTLD"] = int(
        any(domain.endswith(tld) for tld in trusted_tlds)
    )

    # =========================
    # 🔗 SHORTENER
    # =========================
    shorteners = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd"]
    features["IsShortened"] = int(
        any(s in domain for s in shorteners)
    )

    # =========================
    # 🧼 FINAL CLEANUP (CRITICAL)
    # =========================
    for key in features:
        if features[key] is None or features[key] == float("inf"):
            features[key] = 0

    return features