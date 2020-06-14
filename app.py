import sqlite3
from flask import Flask, render_template

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row #To have name-based access to columns
    return conn

app = Flask(__name__)

@app.route('/')
def home():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('home.html', items=items)
