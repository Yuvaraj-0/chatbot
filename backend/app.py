from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


OPENROUTER_API_KEY = "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"
MODEL_ID = "openai/gpt-oss-120b"

def chatbot_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        return f"Error: {response.text}"
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"]

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        prompt = data.get("prompt")
        print("Received prompt:", prompt)
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        reply = chatbot_response(prompt)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=3002, debug=True)
