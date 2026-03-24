from database import get_db

def create_tables():
    conn = get_db()
    cur = conn.cursor()

    # admin
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT,
        password TEXT
    )
    """)

    # mijozlar
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        region TEXT,
        bottles INTEGER DEFAULT 0
    )
    """)

    # kuryerlar
    cur.execute("""
    CREATE TABLE IF NOT EXISTS couriers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        region TEXT
    )
    """)

    # buyurtmalar
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        amount INTEGER,
        region TEXT,
        status TEXT,
        courier_id INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()