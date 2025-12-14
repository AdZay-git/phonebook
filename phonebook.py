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
def add_contact(conn):
    name = input("Имя: ").strip()
    phone = input("Телефон: ").strip()
    email = input("Email (пусто, если нет): ").strip() or None

    conn.execute(
        "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
        (name, phone, email),
    )
    conn.commit()
    print("Контакт добавлен.")

def list_contacts(conn):
    cur = conn.execute("SELECT id, name, phone, email FROM contacts ORDER BY name")
    rows = cur.fetchall()
    if not rows:
        print("Контактов нет.")
        return
    print("\nID | Имя | Телефон | Email")
    print("-" * 40)
    for cid, name, phone, email in rows:
        print(f"{cid} | {name} | {phone} | {email or ''}")

def edit_contact(conn):
    list_contacts(conn)
    cid = input("ID контакта для редактирования: ").strip()
    if not cid.isdigit():
        print("Неверный ID.")
        return
    cid = int(cid)

    cur = conn.execute("SELECT name, phone, email FROM contacts WHERE id = ?", (cid,))
    row = cur.fetchone()
    if not row:
        print("Контакт не найден.")
        return

    name_new = input(f"Новое имя [{row[0]}]: ").strip() or row[0]
    phone_new = input(f"Новый телефон [{row[1]}]: ").strip() or row[1]
    email_new = input(f"Новый email [{row[2] or ''}]: ").strip() or row[2]

    conn.execute(
        "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
        (name_new, phone_new, email_new, cid),
    )
    conn.commit()
    print("Контакт обновлён.")

def delete_contact(conn):
    list_contacts(conn)
    cid = input("ID контакта для удаления: ").strip()
    if not cid.isdigit():
        print("Неверный ID.")
        return
    cid = int(cid)
    conn.execute("DELETE FROM contacts WHERE id = ?", (cid,))
    conn.commit()
    print("Контакт удалён (если существовал).")
def export_json(conn, filename):
    cur = conn.execute("SELECT id, name, phone, email FROM contacts")
    rows = cur.fetchall()
    contacts = [
        {"id": r[0], "name": r[1], "phone": r[2], "email": r[3]}
        for r in rows
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    print(f"Экспортировано в JSON: {filename}")
def export_csv(conn, filename):
    cur = conn.execute("SELECT id, name, phone, email FROM contacts")
    rows = cur.fetchall()
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "phone", "email"])
        writer.writeheader()
        for r in rows:
            writer.writerow({"id": r[0], "name": r[1], "phone": r[2], "email": r[3]})
    print(f"Экспортировано в CSV: {filename}")
def import_json(conn, filename):
    path = Path(filename)
    if not path.exists():
        print("Файл не найден.")
        return
    with open(filename, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    count = 0
    for c in contacts:
        name = c.get("name")
        phone = c.get("phone")
        email = c.get("email")
        if not name or not phone:
            continue
        conn.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email),
        )
        count += 1
    conn.commit()
    print(f"Импортировано из JSON: {count} контактов.")
def import_csv(conn, filename):
    path = Path(filename)
    if not path.exists():
        print("Файл не найден.")
        return
    count = 0
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name")
            phone = row.get("phone")
            email = row.get("email")
            if not name or not phone:
                continue
            conn.execute(
                "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                (name, phone, email),
            )
            count += 1
    conn.commit()
    print(f"Импортировано из CSV: {count} контактов.")
