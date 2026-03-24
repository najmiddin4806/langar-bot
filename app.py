import sqlite3
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import os
import threading
from flask import Flask

app = Flask(__name__)

# ❗ test uchun to‘g‘ridan-to‘g‘ri token
TOKEN = "8349824316:AAFUm18cQjiK2JFwpSwdOuHiPkUcd5Lm8OA"

# ---------------- STATE ----------------
(MENU, COUNT) = range(2)

# ---------------- DB ----------------
conn = sqlite3.connect("water_bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
order_id INTEGER PRIMARY KEY AUTOINCREMENT,
count INTEGER
)
""")
conn.commit()

# ---------------- MENU ----------------
def main_menu():
    return ReplyKeyboardMarkup([
        ["🛒 Yangi buyurtma berish"],
        ["📜 Buyurtmalar tarixi"]
    ], resize_keyboard=True)

# ---------------- HANDLERS ----------------
def start(update, context):
    update.message.reply_text("Asosiy menyu", reply_markup=main_menu())
    return MENU

def menu_handler(update, context):
    text = update.message.text

    if text == "🛒 Yangi buyurtma berish":
        update.message.reply_text("Nechta suv kerak? (2-5)")
        return COUNT

    elif text == "📜 Buyurtmalar tarixi":
        rows = cursor.execute("SELECT * FROM orders").fetchall()
        if not rows:
            update.message.reply_text("Buyurtmalar yo‘q ❗")
        else:
            text = "📜 Buyurtmalar:\n"
            for r in rows:
                text += f"{r[0]}-ID | {r[1]} ta\n"
            update.message.reply_text(text)
        return MENU

    return MENU

def count(update, context):
    try:
        c = int(update.message.text)
    except:
        update.message.reply_text("Son kiriting ❗")
        return COUNT

    cursor.execute("INSERT INTO orders(count) VALUES(?)", (c,))
    conn.commit()

    update.message.reply_text(f"{c} ta buyurtma saqlandi ✅", reply_markup=main_menu())
    return MENU

# ---------------- BOT ----------------
def run_bot():
    try:
        print("Bot starting...")

        updater = Updater(TOKEN, use_context=True)

        # ❗ MUHIM: eski update’larni tozalash (conflict bo‘lmasin)
        updater.bot.delete_webhook(drop_pending_updates=True)

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

        # ❗ signal muammosi uchun
        updater.start_polling(drop_pending_updates=True)
        updater.idle()

    except Exception as e:
        print("BOT ERROR:", e)

# ---------------- FLASK ----------------
@app.route("/")
def home():
    return "Admin panel ishlayapti ✅"

# ---------------- RUN ----------------
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 5000))
    print("Flask starting on port:", port)

    app.run(host="0.0.0.0", port=port)
