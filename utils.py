import sqlite3
from datetime import datetime

def insert_absensi(nama):
    conn = sqlite3.connect("database/absensi.db")
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO absensi (nama, tanggal_waktu) VALUES (?, ?)", (nama, now))
    conn.commit()
    conn.close()
    print(f"Absensi {nama} berhasil dicatat!")
