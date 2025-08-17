import google.generativeai as genai

# API key ayarı
genai.configure(api_key="AIzaSyC0KTf7YP1u1ScHLIP3pz3TM0Xt9N1GV-g")

# Her kullanıcı için chat oturumu oluşturmak için dictionary
user_sessions = {}

def get_user_chat(user_id):
    # Eğer kullanıcı için daha önce chat başlatılmamışsa yeni oluştur
    if user_id not in user_sessions:
        model = genai.GenerativeModel("gemini-1.5-pro")  # pro daha iyi, flash daha hızlı
        chat = model.start_chat(history=[])
        user_sessions[user_id] = chat
    return user_sessions[user_id]

def send_message(user_id, message):
    chat = get_user_chat(user_id)
    response = chat.send_message(message)
    return response.text
