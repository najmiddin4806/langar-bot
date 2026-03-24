import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "water_bot.db")

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

cur.execute("""
INSERT INTO orders (client_id,amount,region,status)
VALUES (1,3,'Toshkent','new')
""")

conn.commit()

print("BUYURTMA QO'SHILDI")

conn.close()