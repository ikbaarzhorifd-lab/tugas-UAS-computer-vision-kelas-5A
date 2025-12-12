import cv2
import os

face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")

name = input("Masukkan nama: ")
dataset_path = f"dataset/{name}"

if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

cap = cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        count += 1
        face = gray[y:y+h, x:x+w]

        cv2.imwrite(f"{dataset_path}/{count}.jpg", face)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Capture Dataset", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if count >= 50:
        break

cap.release()
cv2.destroyAllWindows()
print("Dataset berhasil dibuat!")
