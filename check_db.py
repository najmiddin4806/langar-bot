import sqlite3

conn = sqlite3.connect("langar.db")
cur = conn.cursor()

cur.execute("""
INSERT INTO orders (client_id,amount,region,status)
VALUES (1,2,'Toshkent','new')
""")

conn.commit()
conn.close()

print("Buyurtma qo'shildi")