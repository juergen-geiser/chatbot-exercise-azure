from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 1) Stichwort-basierte Intent-Definition
intents = {
    "greeting": ["hallo", "hi", "servus", "guten tag"],
    "farewell": ["tschüss", "bye", "auf wiedersehen"],
    "thanks": ["danke", "thank you"]
}

# 2) Klassifizierungsfunktion
def classify_intent(text: str) -> str:
    tl = text.lower()
    for intent, keywords in intents.items():
        if any(kw in tl for kw in keywords):
            return intent
    return "unknown"

# 3) Home-Route: liefert das Formular
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# 4) Chat-Route: nimmt JSON, klassifiziert und antwortet
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Kein Text angegeben"}), 400

    intent = classify_intent(text)
    if intent == "greeting":
        reply = "Hallo! Wie kann ich dir helfen?"
    elif intent == "farewell":
        reply = "Tschüss! Einen schönen Tag noch."
    elif intent == "thanks":
        reply = "Gern geschehen!"
    else:
        reply = "Entschuldigung, das habe ich nicht verstanden."

    return jsonify({"intent": intent, "reply": reply})

if __name__ == "__main__":
    # Lokaler Test
    app.run(host="0.0.0.0", port=5000, debug=True)
