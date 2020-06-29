from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Item, User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
	losts = Item.query.filter_by(category="lost")
	founds = Item.query.filter_by(category="found")
	return render_template('home.html', losts=losts, founds=founds)

@main.route('/dashboard')
@login_required
def dashboard():
	listings = Item.query.filter_by(lister=current_user)
	return render_template('dashboard.html', name=current_user.name, listings=listings)
