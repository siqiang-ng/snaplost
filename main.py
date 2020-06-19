from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Item
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    items = Item.query.all()
    return render_template('home.html', items=items)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)
