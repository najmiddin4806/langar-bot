import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "water_bot.db")

print("ADMIN PANEL DATABASE:", DB_NAME)

def get_db():
    conn = sqlite3.connect("../water_bot.db")
    conn.row_factory = sqlite3.Row
    return conn