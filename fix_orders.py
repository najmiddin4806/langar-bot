import sqlite3
import os

# BU ADMIN PANEL ICHIDAN ISHLAYDI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "water_bot.db")

print("DB:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("ALTER TABLE orders ADD COLUMN courier_id INTEGER")

conn.commit()
conn.close()

print("courier_id qo‘shildi ✅")