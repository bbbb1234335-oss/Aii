import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8723161762:AAFV_X42DOBc5k4CZUA1nIjecan4LBHSu_U")
GEMINI_API_KEY = os.getenv("AIzaSyBJx_j4uXO2uEkCeotG8BpDdRxsMtgW_Zo")

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def send_message(chat_id, text):
    url = API_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram Send Error: {e}")

def get_ai_reply(user_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"Respond in the same language as the user. If user writes in Bengali, reply in Bengali. If English, reply in English. User message: {user_text}"}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in result:
            return f"❌ API Error: {result['error']['message']}"
        else:
            return "❌ AI কোনো রেসপন্স দিতে পারছে না।"
            
    except Exception as e:
        return f"❌ Gemini API Error: {e}"

def get_updates(offset=None):
    url = API_URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    try:
        response = requests.get(url, params=params)
        return response.json()
    except:
        return {"result": []}

def main():
    print("🤖 বট চালু হয়েছে এবং আপনার মেসেজের অপেক্ষায় আছে...")
    last_update_id = None
    
    while True:
        try:
            updates = get_updates(last_update_id)
            if "result" in updates:
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    if "message" in update:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"].get("text")
                        if text:
                            print(f"👤 User: {text}")
                            reply = get_ai_reply(text)
                            print(f"🤖 Bot: {reply}")
                            send_message(chat_id, reply)
            time.sleep(1)
        except Exception as e:
            print(f"❌ Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()