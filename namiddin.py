import sqlite3
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
import os

TOKEN = "8708657966:AAHYXHbltonZlecgerMSS3ENGJaWFMdaTFs"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "water_bot.db")

print("COURIER BOT DATABASE:", DB_NAME)


def start(update, context):

    user_id = update.message.from_user.id

    update.message.reply_text(
f"""🚚 Kuryer bot ishga tushdi

Sizning Telegram ID:
{user_id}

Bu ID ni admin panelga kiriting."""
    )


def button(update, context):

    query = update.callback_query
    query.answer()

    data = query.data
    print("DATA:", data)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:

        # 🟡 Jarayonda
        if "process_" in data:

            order_id = data.replace("process_", "")

            cur.execute(
                "UPDATE orders SET status='process' WHERE order_id=?",
                (order_id,)
            )
            conn.commit()

            try:
                query.edit_message_text(f"🟡 Jarayonda\nID: {order_id}")
            except:
                pass

        # ✅ Yetkazildi
        elif "done_" in data:

            order_id = data.replace("done_", "")

            print("DONE ISHLADI:", order_id)

            cur.execute(
                "UPDATE orders SET status='done' WHERE order_id=?",
                (order_id,)
            )
            conn.commit()

            try:
                query.edit_message_text(f"✅ Yetkazildi\nID: {order_id}")
            except:
                pass

    except Exception as e:
        print("XATO:", e)

    conn.close()

def main():

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()