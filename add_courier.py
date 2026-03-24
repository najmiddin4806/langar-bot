from database import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("""
INSERT INTO couriers (name, phone, telegram_id)
VALUES ("Namiddin","998901234567",451484554)
""")

conn.commit()
conn.close()

print("Kuryer qo'shildi")