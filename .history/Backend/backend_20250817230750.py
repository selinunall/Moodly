from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import redis

load_dotenv()  # .env dosyasını yükler
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Model seç
model = genai.GenerativeModel("gemini-1.5-flash")

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# RAM'de kullanıcı oturumlarını saklamak için dictionary
user_sessions = {}

prompt="Kullanıcıya psikolojik destek sağlayan bir asistan olarak davranacaksın. Kullanıcıya nazik ve destekleyici şekilde cevap ver. Duygularını, diyaloglardan analiz et. Kullanıcının durumuna göre tavsiyelerde bulun. Kullanıcının ruh halini iyileştirmeye çalışan bir arkadaş gibi davran." 

# Redis key fonksiyonu
def redis_key(user_id: str) -> str:
    return f"chat:{user_id}:history"

# Kullanıcının sohbet geçmişini getir
def get_user_history(user_id: str):
    history_json = redis_client.get(redis_key(user_id))
    if history_json:
        return json.loads(history_json)
    else:
        # Yeni kullanıcı → başlangıç prompt ve model karşılama mesajı
        return [
            {"role": "user", "parts": [{"text": prompt}]},
            {"role": "model", "parts": [{"text": "Merhaba, size nasıl yardımcı olabilirim?"}]}
        ]

# Kullanıcının geçmişini kaydet
def save_user_history(user_id: str, history):
    redis_client.set(redis_key(user_id), json.dumps(history))


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        user_message = data.get("message", "").strip()

        if not user_id or not user_message:
            return jsonify({"error": "user_id ve message zorunlu"}), 400

        # 1) Geçmişi al
        history = get_user_history(user_id)

        # 2) Yeni mesajı geçmişe ekle
        history.append({"role": "user", "parts": [{"text": user_message}]})

        # 3) Modelden yanıt al
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message({"role":"user","parts":[{"text": user_message}]})
        ai_message = response.text

        # 4) AI mesajını da geçmişe ekle
        history.append({"role": "model", "parts": [{"text": ai_message}]})

        # 5) Güncellenmiş geçmişi Redis’e kaydet
        save_user_history(user_id, history)

        return jsonify({"reply": ai_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Backend çalışıyor 🚀"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
