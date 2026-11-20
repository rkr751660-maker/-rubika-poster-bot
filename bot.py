# -*- coding: utf-8 -*-
import re
from rubiko import RubikaSelfBot

# اتصال به اکانت با استفاده از فایل کلید (session.db)
selfbot = RubikaSelfBot(session_path="session.db")

def process_text(text):
    clean_text = re.sub(r'@\w+', '', text).strip()
    return f"**{clean_text}**\n\n👉 [@AHANG_1R](https://rubika.ir/AHANG_1R)"

CHANNELS = {}
user_states = {}

@selfbot.on_message()
def handle_message(message):
    text = message.text.strip() if message.text else ""
    chat_id = message.chat_id

    if text == "/start":
        user_states[chat_id] = {}
        selfbot.send_message(chat_id, "سلام! 👋\nبرای ارسال پست، **متن** یا **عکس** خود را بفرستید.")
        return

    if text.startswith("/add_channel"):
        parts = text.split(" ", 3)
        if len(parts) >= 3:
            num = parts[1]
            channel_id = parts[2]
            channel_name = parts[3] if len(parts) > 3 else f"کانال {num}"
            CHANNELS[num] = {"name": channel_name, "id": channel_id}
            selfbot.send_message(chat_id, f"✅ کانال {num} ذخیره شد.")
        return

    if chat_id not in user_states:
        if not CHANNELS:
            selfbot.send_message(chat_id, "⚠️ ابتدا با /add_channel کانال را ثبت کنید.")
            return
        user_states[chat_id] = {"text": text}
        selfbot.send_message(chat_id, "📌 شماره کانال مقصد را بفرستید:\n" + "\n".join([f"{k}: {v['name']}" for k, v in CHANNELS.items()]))
        return

    if text in CHANNELS:
        target = CHANNELS[text]["id"]
        saved_text = user_states[chat_id]["text"]
        selfbot.send_message(target, process_text(saved_text))
        selfbot.send_message(chat_id, "✅ پست شد.")
        del user_states[chat_id]

if __name__ == "__main__":
    print("🤖 ربات سلف‌بات روشن شد...")
    selfbot.run()
