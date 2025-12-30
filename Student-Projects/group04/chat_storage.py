import sqlite3
import os
import json
from datetime import datetime

DB_DIR = "chats"
DB_PATH = os.path.join(DB_DIR, "chats.db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def init_db(clear_existing=False):
    with sqlite3.connect(DB_PATH) as conn:
        if clear_existing:
            conn.execute("DROP TABLE IF EXISTS chats")
            conn.commit()

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                smart_title TEXT,
                messages TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        try:
            conn.execute("SELECT smart_title FROM chats LIMIT 1")
        except sqlite3.OperationalError:
            print("ستون smart_title وجود نداشت — در حال اضافه کردن...")
            conn.execute("ALTER TABLE chats ADD COLUMN smart_title TEXT")
            print("ستون smart_title با موفقیت اضافه شد!")

        conn.commit()

def delete_all_chats():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM chats")
        conn.commit()

def save_chat(messages, title, smart_title=None):
    """ایجاد یک چت جدید با عنوان منحصر به فرد"""
    data = json.dumps(messages, ensure_ascii=False)
    now = datetime.now()
    
    unique_title = f"{title} {now.strftime('%Y%m%d_%H%M%S_%f')}"
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO chats (title, smart_title, messages, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (unique_title, smart_title, data, now.isoformat(), now.isoformat()))
        conn.commit()
    
    return unique_title

def create_new_chat():
    """ایجاد یک چت جدید با عنوان منحصر به فرد"""
    save_chat([], "چت جدید")
    all_chats = load_all_chats()
    return all_chats[0] if all_chats else None

def load_all_chats():
    """بارگذاری همه چت‌ها به ترتیب آخرین بروزرسانی"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT id, title, smart_title, messages, updated_at FROM chats
            ORDER BY updated_at DESC
        """).fetchall()

    chats = []
    for row in rows:
        try:
            chats.append({
                "id": row["id"],
                "title": row["title"],
                "smart_title": row["smart_title"],
                "messages": json.loads(row["messages"]),
                "updated_at": row["updated_at"]
            })
        except json.JSONDecodeError as e:
            print(f"خطا در بارگذاری چت {row['title']}: {e}")
    return chats

def update_chat(chat_id, messages, smart_title=None):
    """بروزرسانی محتوای یک چت موجود"""
    data = json.dumps(messages, ensure_ascii=False)
    now = datetime.now().isoformat()
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            UPDATE chats 
            SET messages = ?, smart_title = ?, updated_at = ?
            WHERE id = ?
        """, (data, smart_title, now, chat_id))
        conn.commit()

def delete_chat(chat_id):
    """حذف یک چت خاص"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
        conn.commit()

init_db()