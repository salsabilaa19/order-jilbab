from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "adminjilbab"

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()
conn.execute("""
CREATE TABLE IF NOT EXISTS pesanan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    jenis_jilbab TEXT,
    warna TEXT,
    jumlah INTEGER,
    alamat TEXT,
    whatsapp TEXT,
    tanggal TEXT
)
""")
conn.commit()
conn.close()

# ================= HALAMAN PEMBELI =================
@app.route("/", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        conn = get_db()
        conn.execute("""
        INSERT INTO pesanan VALUES (NULL,?,?,?,?,?,?,?)
        """, (
            request.form["nama"],
            "Jilbab Paris Ori",
            request.form["warna"],
            request.form["jumlah"],
            request.form["alamat"],
            request.form["whatsapp"],
            datetime.now().strftime("%d-%m-%Y %H:%M")
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("sukses"))

    return render_template("order.html")

@app.route("/sukses")
def sukses():
    return "<h2>Pesanan berhasil dikirim 😊</h2>"

# ================= LOGIN ADMIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "12345":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return "Login gagal"

    return render_template("login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = get_db()
    data = conn.execute("SELECT * FROM pesanan ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================= RUN =================
import os

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
