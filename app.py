import sqlite3
import os
from flask import Flask, render_template, session, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row #To have name-based access to columns
    return conn

def get_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?',
                        (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('home.html', items=items)

@app.route('/<int:item_id>')
def item(item_id):
    item = get_item(item_id)
    return render_template('item.html', item=item)

@app.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('create.html')
