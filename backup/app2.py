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
    if request.method == 'POST':
        item = request.form['item']
        description = request.form['description']
        occurdate = request.form['occurdate']
        time = request.form['time']
        photo = request.form['photo']

        if not item:
            flash('Item name is required!')
            return render_template('create.html')
        if not description:
            flash('Item description is required!')
            return render_template('create.html')
        if not photo:
            flash('Photo of the item is required!')
            return render_template('create.html')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO items (item, description, occurdate, time, photo) VALUES (?, ?, ?, ?, ?)',
                    (item, description, occurdate, time, photo))
            conn.commit()
            conn.close()
            flash('"{}" is successfully listed!'.format(item))
            return redirect(url_for('home'))
    else:
        return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    item = get_item(id)
    
    if request.method == 'POST':
        name = request.form['item']
        description = request.form['description']
        occurdate = request.form['occurdate']
        time = request.form['time']
        photo = request.form['photo']

        if not name:
            flash('Item name is required!')
            return render_template('edit.html', item=item)
        if not description:
            flash('Item description is required!')
            return render_template('edit.html', item=item)
        if not photo:
            flash('Photo of the item is required!')
            return render_template('edit.html', item=item)
        else:
            conn = get_db_connection()
            conn.execute('UPDATE items SET item = ?, description = ?, occurdate = ?, time = ?, photo =?' 
                    'WHERE id = ?', (name, description, occurdate, time, photo, id))
            conn.commit()
            conn.close()
            flash('"{}" is successfully edited!'.format(name))
        return redirect(url_for('home'))
    else:
        return render_template('edit.html', item=item)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    item = get_item(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(item['item']))
    return redirect(url_for('home'))
