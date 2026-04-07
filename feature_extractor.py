from urllib.parse import urlparse
import re
import math

def shannon_entropy(s):
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    return -sum([p * math.log2(p) for p in prob])

def extract_features(url):
    features = {}

    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    # ── Basic ─────────────────────────────
    features["URLLength"] = len(url)
    features["DomainLength"] = len(domain)

    # ── IP address ───────────────────────
    features["IsDomainIP"] = 1 if re.match(r"\d+\.\d+\.\d+\.\d+", domain) else 0

    # ── HTTPS ────────────────────────────
    features["IsHTTPS"] = 1 if parsed.scheme == "https" else 0

    # ── Subdomains ───────────────────────
    features["NoOfSubDomain"] = domain.count(".")

    # ── Obfuscation ──────────────────────
    features["HasObfuscation"] = 1 if "%" in url else 0

    # ── Special characters ───────────────
    features["NoOfEqualsInURL"] = url.count("=")
    features["NoOfQMarkInURL"] = url.count("?")
    features["NoOfAmpersandInURL"] = url.count("&")
    features["NoOfAtInURL"] = url.count("@")
    features["NoOfHyphenInURL"] = url.count("-")

    # ── Digits ───────────────────────────
    digits = sum(c.isdigit() for c in url)
    features["NoOfDigitsInURL"] = digits
    features["DigitRatioInURL"] = digits / len(url) if len(url) > 0 else 0

    # ── Letters ──────────────────────────
    letters = sum(c.isalpha() for c in url)
    features["NoOfLettersInURL"] = letters
    features["LetterRatioInURL"] = letters / len(url) if len(url) > 0 else 0

    # ── Suspicious keywords ──────────────
    suspicious_words = [
        "login", "verify", "update", "bank", "secure",
        "account", "free", "bonus", "signin", "confirm"
    ]
    features["HasSuspiciousWord"] = int(
        any(word in url.lower() for word in suspicious_words)
    )

    # ── Suspicious TLD ───────────────────
    suspicious_tlds = [".tk", ".ml", ".ga", ".cf", ".xyz"]
    features["HasSuspiciousTLD"] = int(
        any(domain.endswith(tld) for tld in suspicious_tlds)
    )

    # ── Path length ──────────────────────
    features["PathLength"] = len(path)

    # ── URL entropy (random-looking URLs) ─
    features["URLEntropy"] = shannon_entropy(url) if len(url) > 0 else 0

    return features