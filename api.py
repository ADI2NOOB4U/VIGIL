from flask import Flask, request, jsonify
from flask_cors import CORS
from phishing_detector import check_phishing

app = Flask(__name__)

# 🔥 FIXED CORS (handles extension + preflight)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# 🔥 STORE LAST URL FROM EXTENSION
last_url_store = {"url": None}


@app.route("/")
def home():
    return "VIGIL API is running 🚀"


# 🔥 EXTENSION ROUTE (WITH OPTIONS SUPPORT)
@app.route("/extension", methods=["POST", "OPTIONS"])
def extension_input():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL"}), 400

    last_url_store["url"] = data["url"]
    print("EXTENSION URL RECEIVED:", data["url"])  # debug

    return jsonify({"status": "received"})


# 🔥 GET LAST URL (for Streamlit)
@app.route("/last_url", methods=["GET"])
def get_last_url():
    url = last_url_store["url"]
    last_url_store["url"] = None
    print("LAST URL FETCHED:", url)  # debug
    return jsonify({"url": url})


# 🔥 SCAN ROUTE (WITH OPTIONS SUPPORT)
@app.route("/scan", methods=["POST", "OPTIONS"])
def scan():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data.get("url")

    result = check_phishing(url)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)