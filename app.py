from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)

# HF-Pipeline: deutschsprachige Sentiment-Analyse (Beispielmodell)
classifier = pipeline(
    "sentiment-analysis",
    model="oliverguhr/german-sentiment-bert"
)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        # Inline-Antwort mit Fehlercode 400
        return jsonify({"error": "Kein Text angegeben"}), 400

    # Führe die Klassifikation durch
    result = classifier(text)
    # Beispiel: [{"label": "POSITIVE", "score": 0.97}]
    return jsonify(result)

if __name__ == "__main__":
    # Nur hier wird der Server gestartet – einmalig!
    app.run(host="0.0.0.0", port=5000, debug=True)