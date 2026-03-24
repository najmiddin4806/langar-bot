import sqlite3
from telegram import *
from telegram.ext import *
import os
import threading
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("8349824316:AAFUm18cQjiK2JFwpSwdOuHiPkUcd5Lm8OA")

# ---------------- BOT ----------------

(
LANG,FISH,PHONE,EXTRA_PHONE,ADD_PHONE,LOCATION,ADDRESS,
REGION_REGISTER,REGISTER_CONFIRM,MENU,COUNT,CONFIRM
)=range(12)

prices = {
"Navoiy (Navoiy shahar)":13000,
"Navoiy (Xatirchi markaz)":11000,
"Navoiy (Xatirchi Lenin)":12000,
"Samarqand (Ishtixon Metan Kattaqorgon)":14000,
"Samarqand (Narpay Mirbozor Oqtosh)":13000,
"Toshkent":23000
}

regions=list(prices.keys())

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


def main_menu():
    return ReplyKeyboardMarkup([
        ["🆔 ID raqam","📜 Buyurtmalar tarixi"],
        ["📦 Bo‘sh baklashkalar","🎁 Bonuslar"],
        ["🛒 Yangi buyurtma berish"]
    ],resize_keyboard=True)


def start(update,context):
    update.message.reply_text("Asosiy menyu",reply_markup=main_menu())
    return MENU


def menu_handler(update,context):
    text=update.message.text

    if text=="🛒 Yangi buyurtma berish":
        update.message.reply_text(
            "Suv miqdorini tanlang",
            reply_markup=ReplyKeyboardMarkup([["2","3","4","5"]],resize_keyboard=True)
        )
        return COUNT

    return MENU


def count(update,context):
    count=int(update.message.text)
    price=13000
    total=count*price

    context.user_data["count"]=count

    update.message.reply_text(
        f"{count} ta suv buyurtma qilindi ✅",
        reply_markup=main_menu()
    )

    return MENU


def run_bot():
    updater=Updater(TOKEN,use_context=True)
    dp=updater.dispatcher

    conv=ConversationHandler(
        entry_points=[CommandHandler("start",start)],
        states={
            MENU:[MessageHandler(Filters.text,menu_handler)],
            COUNT:[MessageHandler(Filters.text,count)],
        },
        fallbacks=[CommandHandler("start",start)]
    )

    dp.add_handler(conv)

    updater.start_polling()
    updater.idle()


# ---------------- FLASK ----------------

@app.route("/")
def home():
    return "Admin panel ishlayapti ✅"


# ---------------- RUN ----------------

if __name__=="__main__":
    threading.Thread(target=run_bot).start()

    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
