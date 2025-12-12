from flask import Flask, render_template
import sqlite3
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database/absensi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM absensi ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", data=data)

@app.route("/camera")
def camera():
    return render_template("camera.html")

@app.route("/start_camera", methods=["POST"])
def start_camera():
    subprocess.Popen(["python", "recognize_live.py"])
    return render_template("camera.html")

if __name__ == "__main__":
    app.run(debug=True)
