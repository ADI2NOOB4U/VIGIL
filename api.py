from flask import Flask, request, jsonify
from flask_cors import CORS
from phishing_detector import check_phishing

app = Flask(__name__)
CORS(app)

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = check_phishing(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000)