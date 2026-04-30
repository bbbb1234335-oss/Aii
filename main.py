import requests
import json
import time

# এখানে আপনার তথ্যগুলো
BOT_TOKEN = "8723161762:AAGt2nsdZmOvfUAhlqyCr9AY3mNc8M4FnEI"
GEMINI_API_KEY = "AIzaSyBKNyyGPjlYyKEsc_v5hFtEGT-DBecjF64"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def send_message(chat_id, text):
    url = API_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram Send Error: {e}")

def get_ai_reply(user_text):
    # মডেল নাম পরিবর্তন করে gemini-1.5-flash দেয়া হয়েছে
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": user_text}]}]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()

        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in result:
            print(f"API Error: {result['error']['message']}")
            return f"❌ API Error: {result['error']['message']}"
        else:
            return "❌ AI কিছু বলতে পারছে না। কোটা শেষ বা সেফটি ইস্যু হতে পারে।"
            
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
    print("বট চালু হয়েছে...")
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
                            print(f"User says: {text}")
                            reply = get_ai_reply(text)
                            send_message(chat_id, reply)
            time.sleep(1)
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
