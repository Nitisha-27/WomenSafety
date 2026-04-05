from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sos_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL,
            lon REAL
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add_contact', methods=['POST'])
def add_contact():
    data = request.json
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)",
                   (data['name'], data['phone']))

    conn.commit()
    conn.close()
    return jsonify({"message": "Saved"})

@app.route('/get_contacts')
def get_contacts():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/sos', methods=['POST'])
def sos():
    data = request.json
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO sos_logs (lat, lon) VALUES (?, ?)",
                   (data['lat'], data['lon']))

    conn.commit()
    conn.close()
    return jsonify({"message": "Logged"})

@app.route('/analytics')
def analytics():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM contacts")
    contacts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sos_logs")
    sos_count = cursor.fetchone()[0]

    cursor.execute("SELECT lat, lon FROM sos_logs ORDER BY id DESC LIMIT 1")
    last = cursor.fetchone()

    conn.close()

    return jsonify({
        "contacts": contacts,
        "sos_count": sos_count,
        "last_location": last
    })

if __name__ == "__main__":
    app.run(debug=True)