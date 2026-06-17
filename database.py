import sqlite3

DB_PATH = "bot_database.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id     INTEGER UNIQUE NOT NULL,
            first_name  TEXT,
            username    TEXT,
            language_code TEXT,
            is_bot      INTEGER DEFAULT 0,
            is_blocked  INTEGER DEFAULT 0,
            created_at  TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_users_chat_id ON users(chat_id);

        CREATE TABLE IF NOT EXISTS categories (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL UNIQUE,
            image_id TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            name        TEXT NOT NULL,
            price       TEXT NOT NULL,
            description TEXT NOT NULL,
            image_id    TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    try:
        cursor.execute("PRAGMA table_info(categories)")
        cols = [row[1] for row in cursor.fetchall()]
        if 'image_id' not in cols:
            cursor.execute("ALTER TABLE categories ADD COLUMN image_id TEXT")
            conn.commit()
    except Exception:
        pass
    conn.close()
    print("✅ Barcha jadvallar tayyor")

# ═══════════════════════════════════════════════
#                   USERS
# ═══════════════════════════════════════════════

def insert_user(chat_id, first_name, username, language_code, is_bot, created_at):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT OR IGNORE INTO users
               (chat_id, first_name, username, language_code, is_bot, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (chat_id, first_name, username, language_code, is_bot, created_at)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"insert_user xato: {e}")
        return False
    finally:
        conn.close()

def get_all_users():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, first_name, username, created_at FROM users WHERE is_blocked = 0")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_user_count():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def block_user(chat_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_blocked = 1 WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

# ═══════════════════════════════════════════════
#                KATEGORIYALAR
# ═══════════════════════════════════════════════

def insert_category(name: str, image_path: str = None):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO categories (name, image_id) VALUES (?, ?)",
            (name, image_path)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# 🛠 ESKI HOLATIGA QAYTARILDI: Bu funksiya faqat 2 ta ustun qaytaradi (maxsulot.py xato bermaydi)
def get_all_categories():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ✨ YANGI QO'SHILDI: Bu esa foydalanuvchilar menyusi (rasmli bo'lim) uchun ishlaydi
def get_all_categories_with_images():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, image_id FROM categories ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_category_by_id(category_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, image_id FROM categories WHERE id = ?", (category_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def delete_category(category_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"delete_category xato: {e}")
        return False
    finally:
        conn.close()

# ═══════════════════════════════════════════════
#                  MAHSULOTLAR
# ═══════════════════════════════════════════════

def insert_product(category_id: int, name: str, price: str, description: str, image_id: str):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO products (category_id, name, price, description, image_id)
               VALUES (?, ?, ?, ?, ?)""",
            (category_id, name, price, description, image_id)
        )
        conn.commit()
        print(f"✅ Mahsulot qo'shildi: {name}, category_id={category_id}")
        return True
    except Exception as e:
        print(f"insert_product xato: {e}")
        return False
    finally:
        conn.close()

def get_all_products():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, c.name, p.name, p.price 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        ORDER BY p.category_id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_products_by_category(category_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, name FROM products WHERE category_id = ? ORDER BY id",
            (category_id,)
        )
        rows = cursor.fetchall()
        print(f"🔍 category_id={category_id} uchun {len(rows)} ta mahsulot topildi")
        return rows
    except Exception as e:
        print(f"get_products_by_category xato: {e}")
        return []
    finally:
        conn.close()

def get_product_by_id(product_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, category_id, name, price, description, image_id FROM products WHERE id = ?",
            (product_id,)
        )
        row = cursor.fetchone()
        return row
    except Exception as e:
        print(f"get_product_by_id xato: {e}")
        return None
    finally:
        conn.close()

def delete_product(product_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"delete_product xato: {e}")
        return False
    finally:
        conn.close()

def get_products_with_categories():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.price, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        ORDER BY c.name, p.name
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows