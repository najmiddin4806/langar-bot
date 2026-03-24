from database import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("ALTER TABLE couriers ADD COLUMN telegram_id INTEGER")

conn.commit()
conn.close()

print("telegram_id ustuni qo'shildi")