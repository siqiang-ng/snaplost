from flask import Blueprint, render_template
from . import db

item = Blueprint('item', __name__)

@item.route('/create')
def create():
    return render_template('create.html')

@item.route('/edit')
def edit():
    return render_template('edit.html')

