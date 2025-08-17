from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# API key ayarı
genai.configure(api_key="AIzaSyC0KTf7YP1u1ScHLIP3pz3TM0Xt9N1GV-g")

# Model seç
model = genai.GenerativeModel("gemini-1.5-flash")

# RAM'de kullanıcı oturumlarını saklamak için dictionary
user_sessions = {}

prompt="Kullanıcıya psikolojik destek sağlayan bir asistan olarak davranacaksın. Kullanıcıya nazik ve destekleyici şekilde cevap ver. Duygularını, diyaloglardan analiz et. Kullanıcının durumuna göre tavsiyelerde bulun. Kullanıcının ruh halini iyileştirmeye çalışan bir arkadaş gibi davran." 

def get_user_chat(user_id):
    """
    Kullanıcı için chat oturumunu döndür.
    Yoksa yeni oluşturur.
    """
    if user_id not in user_sessions:
        chat = model.start_chat(history=[{"parts": [{"text": prompt}]}])
        user_sessions[user_id] = chat
    return user_sessions[user_id]

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        user_message = data.get("message", "")

        if not user_id or not user_message:
            return jsonify({"error": "user_id ve message zorunlu"}), 400

        chat_session = get_user_chat(user_id)
        response = chat_session.send_message(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Backend çalışıyor 🚀"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
