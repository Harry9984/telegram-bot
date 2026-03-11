import telebot
import requests
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = (
    "You are Harry personal AI assistant. Harry is a forex trader and trading educator "
    "who runs a brand called The Market Secret. You help Harry with everything including: "
    "Forex analysis on XAUUSD, EURUSD, GBPUSD using Elliott Wave WXY strategy and Fibonacci zones. "
    "Course creation and TikTok content ideas for The Market Secret. "
    "Telegram community growth and student trading questions. "
    "Daily planning, scheduling and productivity. "
    "Health, fitness and workout plans as a personal trainer. "
    "Diet, nutrition and habit tracking. "
    "Motivation and mindset coaching. "
    "General knowledge and advice on any topic. "
    "Always be direct, practical and encouraging. Speak like a trusted personal advisor and coach."
)

def ask_ai(user_message):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        }
    )
    return response.json()["choices"][0]["message"]["content"]

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    reply = ask_ai(message.text)
    bot.reply_to(message, reply)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass

def run_web():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_web, daemon=True).start()
print("Bot is running...")
bot.polling()
