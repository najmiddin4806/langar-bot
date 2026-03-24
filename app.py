from flask import Flask, render_template, request, redirect, session
from database import get_db
from models import create_tables
import requests

import asyncio
import threading
from aiogram import Bot, Dispatcher, types

app = Flask(__name__)
app.secret_key = "secret123"

BOT_TOKEN = "8349824316:AAFUm18cQjiK2JFwpSwdOuHiPkUcd5Lm8OA"

# --- BOT INIT ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

create_tables()


def create_admin():
    conn = get_db()
    cur = conn.cursor()

    admin = cur.execute(
        "SELECT * FROM admins WHERE login=?",
        ("admin",)
    ).fetchone()

    if not admin:
        cur.execute(
            "INSERT INTO admins (login,password) VALUES (?,?)",
            ("admin","1234")
        )
        conn.commit()

    conn.close()


create_admin()


# ---------------- BOT HANDLER ----------------

@dp.message()
async def start_handler(message: types.Message):
    await message.answer("Langar bot ishlayapti ✅")


def start_bot():
    # 🔥 MUHIM TUZATISH (thread xatosi uchun)
    asyncio.run(dp.start_polling(bot, handle_signals=False))


# ---------------- KURYERLAR ----------------

@app.route("/couriers")
def couriers():
    conn = get_db()
    cur = conn.cursor()

    rows = cur.execute("SELECT * FROM couriers").fetchall()

    return render_template("couriers.html", couriers=rows)


@app.route("/add_courier", methods=["POST"])
def add_courier():
    name = request.form["name"]
    phone = request.form["phone"]
    region = request.form["region"]
    telegram_id = request.form["telegram_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO couriers(name,phone,region,telegram_id)
    VALUES(?,?,?,?)
    """,(name,phone,region,telegram_id))

    conn.commit()

    return redirect("/couriers")


# ---------------- LOGIN ----------------

@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    login = request.form["login"]
    password = request.form["password"]

    conn = get_db()
    cur = conn.cursor()

    admin = cur.execute(
        "SELECT * FROM admins WHERE login=? AND password=?",
        (login,password)
    ).fetchone()

    if admin:
        session["admin"] = admin["id"]
        return redirect("/dashboard")

    return "Login xato"


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    conn = get_db()
    cur = conn.cursor()

    total = cur.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    new = cur.execute("SELECT COUNT(*) FROM orders WHERE status='new'").fetchone()[0]
    process = cur.execute("SELECT COUNT(*) FROM orders WHERE status='process'").fetchone()[0]
    done = cur.execute("SELECT COUNT(*) FROM orders WHERE status='done'").fetchone()[0]

    return render_template(
        "dashboard.html",
        total=total,
        new=new,
        process=process,
        done=done
    )


# ---------------- BUYURTMALAR ----------------

@app.route("/orders")
def orders():

    conn = get_db()
    cur = conn.cursor()

    orders = cur.execute("""
    SELECT 
        orders.order_id,
        users.fish,
        users.phone,
        orders.count,
        orders.region
    FROM orders
    LEFT JOIN users
    ON orders.user_id = users.user_id
    """).fetchall()

    couriers = cur.execute("SELECT * FROM couriers").fetchall()

    return render_template("orders.html", orders=orders, couriers=couriers)


# ---------------- KURYERGA YUBORISH ----------------

@app.route("/assign",methods=["POST"])
def assign():

    order_id = request.form["order_id"]
    courier_id = request.form["courier_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
    "UPDATE orders SET courier_id=?,status='process' WHERE order_id=?",
    (courier_id,order_id)
    )

    courier = cur.execute(
        "SELECT * FROM couriers WHERE id=?",
        (courier_id,)
    ).fetchone()

    order = cur.execute(
        "SELECT * FROM orders WHERE order_id=?",
        (order_id,)
    ).fetchone()

    conn.commit()

    send_order_to_courier(courier["telegram_id"], order)

    return redirect("/orders")


# ---------------- TELEGRAMGA YUBORISH ----------------

def send_order_to_courier(chat_id, order):

    text = f"""
🚚 Yangi buyurtma

📦 Buyurtma ID: {order['order_id']}
💧 Suv: {order['count']}
📍 Hudud: {order['region']}
"""

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🟡 Jarayonda", "callback_data": f"process_{order['order_id']}"},
                {"text": "✅ Yetkazildi", "callback_data": f"done_{order['order_id']}"}
            ]
        ]
    }

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "reply_markup": keyboard
    })


# ---------------- RUN ----------------

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=5000)
