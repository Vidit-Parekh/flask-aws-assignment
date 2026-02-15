from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'mysecretkey'

UPLOAD_FOLDER = '/home/ubuntu/flaskapp/uploads'
DB_PATH = '/home/ubuntu/flaskapp/users.db'

# ── Initialize Database ─────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        username  TEXT NOT NULL UNIQUE,
        password  TEXT NOT NULL,
        firstname TEXT,
        lastname  TEXT,
        email     TEXT,
        address   TEXT,
        limerick  TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# ── Route 1: Home → Registration Page ──────────────────────────
@app.route('/')
def index():
    return render_template('register.html')

# ── Route 2: Handle Registration Form ──────────────────────────
@app.route('/register', methods=['POST'])
def register():
    username  = request.form['username']
    password  = request.form['password']
    firstname = request.form['firstname']
    lastname  = request.form['lastname']
    email     = request.form['email']
    address   = request.form['address']

    limerick_text = ''
    if 'limerick' in request.files:
        file = request.files['limerick']
        if file and file.filename != '':
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            with open(filepath, 'r') as f:
                limerick_text = f.read()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password, firstname, lastname, email, address, limerick) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, password, firstname, lastname, email, address, limerick_text)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return render_template('register.html', error="Username already taken! Try another.")
    conn.close()

    return redirect(url_for('profile', username=username))

# ── Route 3: Profile Display Page ──────────────────────────────
@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if not user:
        return redirect(url_for('login'))

    word_count = len(user[7].split()) if user[7] else 0
    return render_template('profile.html', user=user, word_count=word_count)

# ── Route 4: Download Limerick File ────────────────────────────
@app.route('/download/<username>')
def download(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT limerick FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()

    if row and row[0]:
        filepath = os.path.join(UPLOAD_FOLDER, f'{username}_limerick.txt')
        with open(filepath, 'w') as f:
            f.write(row[0])
        return send_file(filepath, as_attachment=True, download_name='Limerick.txt')
    return "No file found", 404

# ── Route 5: Login Page (GET) ───────────────────────────────────
@app.route('/login')
def login():
    return render_template('login.html')

# ── Route 6: Handle Login Form (POST) ──────────────────────────
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return redirect(url_for('profile', username=username))
    return render_template('login.html', error="Invalid username or password. Try again!")

if __name__ == '__main__':
    app.run(debug=True)
