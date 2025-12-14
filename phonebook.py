import sqlite3
import json
import csv
from pathlib import Path

DB_NAME = "phonebook.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    """)
    conn.commit()
    return conn
