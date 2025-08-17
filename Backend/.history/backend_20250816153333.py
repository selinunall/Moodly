Gemini_Api_Key = AIzaSyC0KTf7YP1u1ScHLIP3pz3TM0Xt9N1GV-g

import google.generativeai as genai

# 1. API key’i ayarla
genai.configure(api_key="AIzaSyC0KTf7YP1u1ScHLIP3pz3TM0Xt9N1GV-g")

# 2. Bir model seç (örnek: Gemini 1.5 Flash)
model = genai.GenerativeModel("gemini-1.5-flash")

# 3. Basit prompt gönder
response = model.generate_content("Merhaba, bana kısa bir şiir yazar mısın?")

# 4. Sonucu yazdır
print(response.text)
