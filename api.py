from flask import Flask, request, jsonify
from flask_cors import CORS
from phishing_detector import check_phishing

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return "VIGIL API is running 🚀"

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data.get("url")

    result = check_phishing(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)