from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 1. API key ayarı
genai.configure(api_key="AIzaSyC0KTf7YP1u1ScHLIP3pz3TM0Xt9N1GV-g")

# 2. Model seç
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Frontend'den gelen veriyi al
        data = request.get_json()
        user_message = data.get("message", "")

        # Gemini API'ye gönder
        response = model.generate_content(user_message)

        # Cevabı frontend'e döndür
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
