import cv2
import time
import sqlite3
from datetime import datetime

# ==========================
# Fungsi Anti-Duplikasi Absen (1x per hari)
# ==========================
def insert_absensi(name):
    conn = sqlite3.connect("database/absensi.db")
    cursor = conn.cursor()

    # Cek apakah nama sudah absen hari ini
    cursor.execute("""
        SELECT * FROM absensi
        WHERE nama = ?
        AND date(tanggal_waktu) = date('now')
    """, (name,))

    sudah_absen = cursor.fetchone()

    if sudah_absen:
        print(f"[INFO] {name} sudah absen hari ini. Tidak dicatat ulang.")
        conn.close()
        return False

    # Jika belum absen, masukkan data
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO absensi (nama, tanggal_waktu)
        VALUES (?, ?)
    """, (name, waktu))

    conn.commit()
    conn.close()
    
    print(f"[INFO] Absensi {name} dicatat pada {waktu}.")
    return True


# ==========================
# Load Cascade & Model
# ==========================
face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("training/model.yml")

# Load labels (ID → Name)
label_dict = {}
with open("training/labels.txt", "r") as f:
    for line in f:
        id_, name = line.strip().split(",")
        label_dict[int(id_)] = name

# ==========================
# Kamera
# ==========================
cap = cv2.VideoCapture(0)

# Hindari spam deteksi (cooldown 5–10 detik)
last_detect = {}
cooldown = 5  # detik

print("[INFO] Kamera berjalan. Tekan 'q' untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca kamera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(face)

        if confidence < 60:  
            name = label_dict[id_]
            now = time.time()

            # COOL DOWN cek wajah (biar teks tidak berkedip terus)
            if name not in last_detect or (now - last_detect[name]) > cooldown:
                last_detect[name] = now

                # Catat absensi jika belum absen hari ini
                insert_absensi(name)

            text = f"{name} ({int(confidence)}%)"
        else:
            text = "Unknown"

        # Kotak & Nama di layar
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, text, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Tampilkan kamera
    cv2.imshow("Recognize Live", frame)

    # Tekan q untuk berhenti
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("[INFO] Kamera dimatikan.")
