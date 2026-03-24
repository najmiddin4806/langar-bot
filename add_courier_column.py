from database import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("ALTER TABLE orders ADD COLUMN courier_id INTEGER")

conn.commit()
conn.close()

print("courier_id ustuni qo'shildi")