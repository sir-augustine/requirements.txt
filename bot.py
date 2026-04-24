import os
import telebot
import google.generativeai as genai
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_prediction(prompt):
    today = datetime.now().strftime("%A, %B %d, %Y")
    full_prompt = f"""You are an expert football analyst and betting tipster.
Today is {today}.
When giving predictions use current form, head-to-head stats, home/away records.
Always include approximate odds. Use emojis. End with gambling reminder.
{prompt}"""
    response = model.generate_content(full_prompt)
    return response.text

@bot.message_handler(commands=["start","help"])
def start(message):
    bot.send_message(message.chat.id,
        "⚽ *Welcome to FootballPredictBot!*\n\n"
        "*Commands:*\n"
        "🏆 /predict — Match winner tips\n"
        "🎯 /accumulator — 5-game accumulator\n"
        "⚽ /btts — Both Teams To Score\n"
        "📊 /overunder — Over/Under goals\n"
        "🔀 /mixed — Mixed prediction slip",
        parse_mode="Markdown")

@bot.message_handler(commands=["predict"])
def predict(message):
    bot.send_message(message.chat.id, "🔍 Analysing matches...")
    bot.send_message(message.chat.id, get_prediction("Give 3 strong match winner 1X2 football predictions for today with league, teams, pick, reasoning and odds."))

@bot.message_handler(commands=["accumulator"])
def accumulator(message):
    bot.send_message(message.chat.id, "🎯 Building accumulator...")
    bot.send_message(message.chat.id, get_prediction("Build a 5-game accumulator where each odd is between 1.20-1.40 and total combined odds equal approximately 3.00. Show each game, tip, odds and reasoning."))

@bot.message_handler(commands=["btts"])
def btts(message):
    bot.send_message(message.chat.id, "⚽ Finding BTTS tips...")
    bot.send_message(message.chat.id, get_prediction("Give 4 Both Teams To Score Yes predictions for today with league, teams, reasoning and odds."))

@bot.message_handler(commands=["overunder"])
def overunder(message):
    bot.send_message(message.chat.id, "📊 Analysing goals...")
    bot.send_message(message.chat.id, get_prediction("Give 4 Over/Under goals predictions for today mixing Over 2.5 and Under 2.5 with reasoning and odds."))

@bot.message_handler(commands=["mixed"])
def mixed(message):
    bot.send_message(message.chat.id, "🔀 Generating mixed slip...")
    bot.send_message(message.chat.id, get_prediction("Give a mixed 5-game prediction slip mixing 1X2, BTTS and Over/Under markets. Each odd 1.20-1.50. Show total combined odds."))

@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    bot.send_message(message.chat.id, "⚽ Analysing...")
    bot.send_message(message.chat.id, get_prediction(f"User asks: '{message.text}'. Give detailed football prediction response."))

if __name__ == "__main__":
    print("Bot running...")
    bot.infinity_polling()
