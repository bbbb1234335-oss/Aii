import requests
import json

BOT_TOKEN = "8723161762:AAGt2nsdZmOvfUAhlqyCr9AY3mNc8M4FnEI"
GEMINI_API_KEY = "AIzaSyC26-gTZ4V0D_v_4eMHM3esUhbZ1BhJ7Q0"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def send_message(chat_id, text):
    url = API_URL + "sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, data=data)

def get_ai_reply(user_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": user_text}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "❌ AI reply failed!"

def get_updates(offset=None):
    url = API_URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def main():
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)

        for update in updates["result"]:
            last_update_id = update["update_id"] + 1

            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text")

                if text:
                    reply = get_ai_reply(text)
                    send_message(chat_id, reply)

if __name__ == "__main__":
    main()