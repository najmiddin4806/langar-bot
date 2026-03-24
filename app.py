import sqlite3
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import os
import threading
from flask import Flask

app = Flask(__name__)

# 🔐 vaqtincha TOKEN (keyin env ga qaytaramiz)
TOKEN = "8349824316:AAFUm18cQjiK2JFwpSwdOuHiPkUcd5Lm8OA"

# ---------------- BOT ----------------

(LANG,FISH,PHONE,EXTRA_PHONE,ADD_PHONE,LOCATION,ADDRESS,
 REGION_REGISTER,REGISTER_CONFIRM,MENU,COUNT,CONFIRM) = range(12)

DB_NAME = "water_bot.db"

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
user_id INTEGER,lang TEXT,fish TEXT,phone TEXT,
extra_phone TEXT,location TEXT,house TEXT,region TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
order_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,region TEXT,count INTEGER,
price INTEGER,status TEXT DEFAULT 'new',date TEXT)""")

conn.commit()


# ---------------- MENU ----------------

def main_menu():
    return ReplyKeyboardMarkup([
        ["🆔 ID raqam","📜 Buyurtmalar tarixi"],
        ["📦 Bo‘sh baklashkalar","🎁 Bonuslar"],
        ["🛒 Yangi buyurtma berish"]
    ], resize_keyboard=True)


# ---------------- HANDLERS ----------------

def start(update, context):
    update.message.reply_text("Asosiy menyu", reply_markup=main_menu())
    return MENU


def menu_handler(update, context):
    text = update.message.text

    if text == "🛒 Yangi buyurtma berish":
        update.message.reply_text(
            "Suv miqdorini tanlang",
            reply_markup=ReplyKeyboardMarkup([["2","3","4","5"]], resize_keyboard=True)
        )
        return COUNT

    elif text == "📜 Buyurtmalar tarixi":
        update.message.reply_text("📜 Hozircha bo‘sh")
        return MENU

    return MENU


def count(update, context):
    try:
        count = int(update.message.text)
    except:
        update.message.reply_text("Iltimos son kiriting ❗")
        return COUNT

    context.user_data["count"] = count

    update.message.reply_text(
        f"{count} ta suv buyurtma qilindi ✅",
        reply_markup=main_menu()
    )

    return MENU


# ---------------- BOT RUN ----------------

def run_bot():
    try:
        print("Bot starting...")

        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher

        conv = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                MENU: [MessageHandler(Filters.text, menu_handler)],
                COUNT: [MessageHandler(Filters.text, count)],
            },
            fallbacks=[CommandHandler("start", start)]
        )

        dp.add_handler(conv)

        updater.start_polling()
        updater.idle()

    except Exception as e:
        print("BOT ERROR:", e)


# ---------------- FLASK ----------------

@app.route("/")
def home():
    return "Admin panel ishlayapti ✅"


# ---------------- RUN ----------------

if __name__ == "__main__":
    # botni alohida threadda ishga tushiramiz
    threading.Thread(target=run_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 5000))
    print("Flask starting on port:", port)

    app.run(host="0.0.0.0", port=port)
