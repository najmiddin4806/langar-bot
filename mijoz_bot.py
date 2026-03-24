import sqlite3
from telegram import *
from telegram.ext import *
import os

TOKEN = "8349824316:AAFUm18cQjiK2JFwpSwdOuHiPkUcd5Lm8OA"

(
LANG,
FISH,
PHONE,
EXTRA_PHONE,
ADD_PHONE,
LOCATION,
ADDRESS,
REGION_REGISTER,
REGISTER_CONFIRM,
MENU,
COUNT,
CONFIRM
) = range(12)

prices = {
"Navoiy (Navoiy shahar)":13000,
"Navoiy (Xatirchi markaz)":11000,
"Navoiy (Xatirchi Lenin)":12000,
"Samarqand (Ishtixon Metan Kattaqorgon)":14000,
"Samarqand (Narpay Mirbozor Oqtosh)":13000,
"Toshkent":23000
}

regions=list(prices.keys())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "water_bot.db")

print("BOT DATABASE:", DB_NAME)

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER,
lang TEXT,
fish TEXT,
phone TEXT,
extra_phone TEXT,
location TEXT,
house TEXT,
region TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
order_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
region TEXT,
count INTEGER,
price INTEGER,
status TEXT DEFAULT 'new',
date TEXT
)
""")

conn.commit()


def main_menu():

    return ReplyKeyboardMarkup([
        ["🆔 ID raqam","📜 Buyurtmalar tarixi"],
        ["📦 Bo‘sh baklashkalar","🎁 Bonuslar"],
        ["🛒 Yangi buyurtma berish"]
    ],resize_keyboard=True)



def start(update,context):

    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (update.message.from_user.id,)
    )

    user=cursor.fetchone()

    if user:

        update.message.reply_text(
            "Asosiy menyu",
            reply_markup=main_menu()
        )

        return MENU


    update.message.reply_text(
"""Assalomu alaykum botimizga hush kelibsiz
Siz bu bot orqali suvga buyurtma berishingiz mumkin""",
reply_markup=ReplyKeyboardMarkup(
[[KeyboardButton("START")]],resize_keyboard=True)
)

    return LANG



def language(update,context):

    btn=[["🇺🇿 Uzbek","🇷🇺 Русский","🇬🇧 English"]]

    update.message.reply_text(
"Tilni tanlang",
reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True)
)

    return FISH



def get_fish(update,context):

    context.user_data["lang"]=update.message.text

    update.message.reply_text("F.I.SH kiriting")

    return PHONE



def get_phone(update,context):

    context.user_data["fish"]=update.message.text

    btn=[[KeyboardButton("Telefon yuborish",request_contact=True)]]

    update.message.reply_text(
"Telefon raqamingizni yuboring",
reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True)
)

    return EXTRA_PHONE



def save_phone(update,context):

    context.user_data["phone"]=update.message.contact.phone_number

    btn=[["Ha","Yo‘q"]]

    update.message.reply_text(
"Qo‘shimcha raqam mavjudmi?",
reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True)
)

    return ADD_PHONE



def add_phone(update,context):

    if update.message.text=="Ha":

        update.message.reply_text("Qo‘shimcha raqam kiriting")

        return ADD_PHONE

    elif update.message.text=="Yo‘q":

        context.user_data["extra"]=""

    else:

        context.user_data["extra"]=update.message.text


    btn=[[KeyboardButton("Lakatsiya yuborish",request_location=True)]]

    update.message.reply_text(
"Manzil yuboring",
reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True)
)

    return LOCATION



def get_location(update,context):

    loc=update.message.location

    context.user_data["location"]=f"{loc.latitude},{loc.longitude}"

    update.message.reply_text(
"Uy manzilini kiriting (masalan 3-podezd 23-xonadon)",
reply_markup=ReplyKeyboardRemove()
)

    return ADDRESS



def finish_address(update,context):

    context.user_data["house"]=update.message.text

    btn=[[r] for r in regions]

    update.message.reply_text(
"Hududni tanlang",
reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True)
)

    return REGION_REGISTER



def register_region(update,context):

    region=update.message.text

    context.user_data["region"]=region

    text=f"""
Ma'lumotlaringizni tekshiring

👤 F.I.SH: {context.user_data['fish']}
📞 Telefon: {context.user_data['phone']}
📞 Qo'shimcha: {context.user_data.get('extra','yo‘q')}
🏠 Manzil: {context.user_data['house']}
📍 Hudud: {region}

Ma'lumotlar to‘g‘rimi?
"""

    btn=[["✅ Ha","✏️ Qayta kiritish"]]

    update.message.reply_text(
text,
reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True)
)

    return REGISTER_CONFIRM



def register_confirm(update,context):

    if update.message.text=="✏️ Qayta kiritish":

        update.message.reply_text(
"Boshidan boshlaymiz.\nF.I.SH kiriting",
reply_markup=ReplyKeyboardRemove()
)

        return PHONE


    elif update.message.text=="✅ Ha":

        cursor.execute("""
INSERT INTO users(
user_id,lang,fish,phone,extra_phone,location,house,region
) VALUES(?,?,?,?,?,?,?,?)
""",(
update.message.from_user.id,
context.user_data["lang"],
context.user_data["fish"],
context.user_data["phone"],
context.user_data.get("extra"),
context.user_data["location"],
context.user_data["house"],
context.user_data["region"]
))

        conn.commit()

        update.message.reply_text(
"Ro‘yxatdan o‘tish yakunlandi",
reply_markup=main_menu()
)

        return MENU



def menu_handler(update,context):

    text=update.message.text


    if text=="🆔 ID raqam":

        cursor.execute(
            "SELECT phone FROM users WHERE user_id=?",
            (update.message.from_user.id,)
        )

        phone=cursor.fetchone()[0]

        update.message.reply_text(
            f"🆔 Sizning ID raqamingiz: {phone}"
        )


    elif text=="📜 Buyurtmalar tarixi":

        cursor.execute(
        "SELECT order_id,region,count,price,date,status FROM orders WHERE user_id=?",
        (update.message.from_user.id,)
        )

        rows=cursor.fetchall()

        if not rows:

            update.message.reply_text("Siz hali buyurtma bermagansiz")

            return MENU

        process=[]
        done=[]

        for r in rows:

            if r[5]=="process":
                process.append(r)
            else:
                done.append(r)

        msg="⏳ Jarayondagi buyurtmalar\n\n"

        for r in process:

            msg+=f"""🆔 ID: {r[0]}
📍 Hudud: {r[1]}
💧 Suv: {r[2]}
💰 Narx: {r[3]}
📅 Sana: {r[4]}

"""

        msg+="\n✅ Yakunlangan buyurtmalar\n\n"

        for r in done:

            msg+=f"""🆔 ID: {r[0]}
📍 Hudud: {r[1]}
💧 Suv: {r[2]}
💰 Narx: {r[3]}
📅 Sana: {r[4]}

"""

        update.message.reply_text(msg)



    elif text=="🎁 Bonuslar":

        cursor.execute(
        "SELECT SUM(count) FROM orders WHERE user_id=? AND status='done'",
        (update.message.from_user.id,)
        )

        total=cursor.fetchone()[0]

        if total is None:
            total=0

        remain=100-total

        update.message.reply_text(
f"""🎁 Bonus tizimi

💧 Jami olingan suv: {total}
🎯 Bonus: 100 ta suv

📊 Bonusgacha qoldi: {remain}
"""
        )


    elif text=="🛒 Yangi buyurtma berish":

        update.message.reply_text(
"Suv miqdorini tanlang",
reply_markup=ReplyKeyboardMarkup([["2","3","4","5"]],resize_keyboard=True)
)

        return COUNT


    return MENU



def count(update,context):

    count=int(update.message.text)

    cursor.execute(
    "SELECT region FROM users WHERE user_id=?",
    (update.message.from_user.id,)
    )

    region=cursor.fetchone()[0]

    price=prices[region]

    total=count*price

    context.user_data["count"]=count
    context.user_data["price"]=total
    context.user_data["region"]=region

    btn=[["Tasdiqlash","Bekor qilish"]]

    update.message.reply_text(
f"{count} x {price} = {total} so‘m",
reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True)
)

    return CONFIRM



def confirm(update,context):

    text = update.message.text

    if text == "Tasdiqlash":

        cursor.execute("""
INSERT INTO orders(user_id,region,count,price,status,date)
VALUES(?,?,?,?,?,datetime('now'))
""",(
update.message.from_user.id,
context.user_data["region"],
context.user_data["count"],
context.user_data["price"],
"new"
))

        conn.commit()

        order_id = cursor.lastrowid

        update.message.reply_text(
f"""✅ Buyurtmangiz qabul qilindi

📦 Buyurtma ID: {order_id}
Tez orada kuryerlarimiz siz bilan bog'lanishadi
""",
reply_markup=main_menu()
)

        return MENU


    elif text == "Bekor qilish":

        update.message.reply_text(
"Buyurtma bekor qilindi",
reply_markup=main_menu()
)

        return MENU


def main():

    updater=Updater(TOKEN)

    dp=updater.dispatcher


    conv=ConversationHandler(

        entry_points=[CommandHandler("start",start)],

        states={

        LANG:[MessageHandler(Filters.text,language)],
        FISH:[MessageHandler(Filters.text,get_fish)],
        PHONE:[MessageHandler(Filters.text,get_phone)],
        EXTRA_PHONE:[MessageHandler(Filters.contact,save_phone)],
        ADD_PHONE:[MessageHandler(Filters.text,add_phone)],
        LOCATION:[MessageHandler(Filters.location,get_location)],
        ADDRESS:[MessageHandler(Filters.text,finish_address)],
        REGION_REGISTER:[MessageHandler(Filters.text,register_region)],
        REGISTER_CONFIRM:[MessageHandler(Filters.text,register_confirm)],
        MENU:[MessageHandler(Filters.text,menu_handler)],
        COUNT:[MessageHandler(Filters.text,count)],
        CONFIRM:[MessageHandler(Filters.text,confirm)]

        },

        fallbacks=[CommandHandler("start",start)]

    )


    dp.add_handler(conv)

    updater.start_polling()

    updater.idle()



if __name__=="__main__":

    main()