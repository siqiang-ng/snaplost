from flask import Blueprint, render_template
from flask_login import login_required
from . import db

item = Blueprint('item', __name__)

@item.route('/create')
@login_required
def create():
    return render_template('create.html')

@item.route('/edit')
@login_required
def edit():
    return render_template('edit.html')

