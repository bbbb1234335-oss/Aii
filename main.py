import requests
import json
import time

# এখানে আপনার সঠিক তথ্যগুলো বসান
BOT_TOKEN = "8723161762:AAGt2nsdZmOvfUAhlqyCr9AY3mNc8M4FnEI"
GEMINI_API_KEY = "AIzaSyBKNyyGPjlYyKEsc_v5hFtEGT-DBecjF64"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def send_message(chat_id, text):
    url = API_URL + "sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram Send Error: {e}")

def get_ai_reply(user_text):
    # মডেল আপডেট করা হয়েছে: gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
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

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()

        # এপিআই থেকে উত্তর খুঁজে বের করা
        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # এরর চেক করার জন্য প্রিন্ট
            print(f"API Error Response: {result}")
            return "❌ AI কিছু বলতে পারছে না (সম্ভবত সেফটি ফিল্টার বা কোটা সমস্যা)।"
            
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "❌ AI reply failed! সার্ভারে সমস্যা হচ্ছে।"

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
                            # স্ক্রিনে ইউজার মেসেজ দেখানোর জন্য
                            print(f"User: {text}")
                            
                            reply = get_ai_reply(text)
                            send_message(chat_id, reply)
            
            # সার্ভারে চাপ কমাতে সামান্য বিরতি
            time.sleep(1)
            
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
    