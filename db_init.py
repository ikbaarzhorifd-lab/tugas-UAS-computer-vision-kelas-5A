import sqlite3

def init_db():
    conn = sqlite3.connect("database/absensi.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS absensi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            tanggal_waktu TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()
    print("Database berhasil dibuat!")

if __name__ == "__main__":
    init_db()
