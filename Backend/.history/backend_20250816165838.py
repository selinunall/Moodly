from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key="YOUR_API_KEY")

user_sessions = {}

def get_user_chat(user_id):
    if user_id not in user_sessions:
        model = genai.GenerativeModel("gemini-1.5-pro")
        chat = model.start_chat(history=[])
        user_sessions[user_id] = chat
    return user_sessions[user_id]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    chat_session = get_user_chat(user_id)
    response = chat_session.send_message(message)

    return jsonify({
        "reply": response.text
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
