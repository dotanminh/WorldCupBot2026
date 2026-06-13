import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "bot_database.db")

def init_db():
    """Khởi tạo cơ sở dữ liệu nếu chưa có."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            chat_id INTEGER PRIMARY KEY,
            username TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Bảng lưu các bài tin tức đã gửi (chống gửi trùng)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent_articles (
            url TEXT PRIMARY KEY,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_subscriber(chat_id, username=None):
    """Thêm người dùng hoặc nhóm vào danh sách nhận tin."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO subscribers (chat_id, username) VALUES (?, ?)", (chat_id, username))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def remove_subscriber(chat_id):
    """Xóa người dùng khỏi danh sách."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscribers WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

def get_all_subscribers():
    """Lấy danh sách tất cả chat_id để gửi tin Broadcast."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM subscribers")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

# ──────────────────────────────────────────
#  Quản lý bài tin đã gửi (chống trùng lặp)
# ──────────────────────────────────────────

def is_article_sent(url):
    """Kiểm tra bài viết đã gửi chưa."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sent_articles WHERE url = ?", (url,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_article_sent(url):
    """Đánh dấu bài viết đã gửi."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO sent_articles (url) VALUES (?)", (url,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def cleanup_old_articles(hours=48):
    """Xóa các bài tin đã gửi quá 48 giờ (giữ DB gọn)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(hours=hours)
    cursor.execute("DELETE FROM sent_articles WHERE sent_at < ?", (cutoff,))
    conn.commit()
    conn.close()

# Tự động tạo bảng khi import file này
init_db()
