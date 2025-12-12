import cv2
import os
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")

dataset_path = "dataset"
faces = []
labels = []
label_dict = {}
current_id = 0

for root, dirs, files in os.walk(dataset_path):
    for dir_name in dirs:
        label_dict[current_id] = dir_name
        folder = os.path.join(dataset_path, dir_name)

        for filename in os.listdir(folder):
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(current_id)

        current_id += 1

recognizer.train(faces, np.array(labels))
recognizer.save("training/model.yml")

with open("training/labels.txt", "w") as f:
    for id_, name in label_dict.items():
        f.write(f"{id_},{name}\n")

print("Training selesai!")
