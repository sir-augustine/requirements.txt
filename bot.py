import os
import telebot
import google.generativeai as genai
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_prediction(prompt):
    today = datetime.now().strftime("%A, %B %d, %Y")
    full_prompt = f"You are an expert football tipster. Today is {today}. {prompt} Use emojis. Include odds."
    response = model.generate_content(full_prompt)
    return response.text

@bot.message_handler(commands=["start","help"])
def start(message):
    bot.send_message(message.chat.id,
        "⚽ Welcome to FootballPredictBot!\n\n"
        "Commands:\n"
        "/predict - Match winner tips\n"
        "/accumulator - 5-game accumulator\n"
        "/btts - Both Teams To Score\n"
        "/overunder - Over/Under goals\n"
        "/mixed - Mixed prediction slip")

@bot.message_handler(commands=["predict"])
def predict(message):
    bot.send_message(message.chat.id, "🔍 Analysing matches...")
    bot.send_message(message.chat.id, get_prediction("Give 3 match winner predictions for today with odds."))

@bot.message_handler(commands=["accumulator"])
def accumulator(message):
    bot.send_message(message.chat.id, "🎯 Building accumulator...")
    bot.send_message(message.chat.id, get_prediction("Build a 5-game accumulator totalling approximately 3.00 odds."))

@bot.message_handler(commands=["btts"])
def btts(message):
    bot.send_message(message.chat.id, "⚽ Finding BTTS tips...")
    bot.send_message(message.chat.id, get_prediction("Give 4 BTTS Yes predictions for today with odds."))

@bot.message_handler(commands=["overunder"])
def overunder(message):
    bot.send_message(message.chat.id, "📊 Analysing goals...")
    bot.send_message(message.chat.id, get_prediction("Give 4 Over/Under predictions for today with odds."))

@bot.message_handler(commands=["mixed"])
def mixed(message):
    bot.send_message(message.chat.id, "🔀 Generating mixed slip...")
    bot.send_message(message.chat.id, get_prediction("Give a mixed 5-game prediction slip with total combined odds."))

@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    bot.send_message(message.chat.id, get_prediction(message.text))

bot.infinity_polling(timeout=60, long_polling_timeout=60)
