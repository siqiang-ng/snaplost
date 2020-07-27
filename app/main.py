from flask import Blueprint, render_template, g, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from app.models import Item, User
from app.forms import SearchForm
from app import db

main = Blueprint('main', __name__)

@main.before_app_request
def before_request():
	g.search_form = SearchForm()
	Item.reindex()

@main.route('/')
def home():
	losts = Item.query.filter_by(category="lost")
	founds = Item.query.filter_by(category="found")
	location = current_app.config['S3_LOCATION'] 
	return render_template('home.html', losts=losts, founds=founds, location=location)


@main.route('/dashboard')
@login_required
def dashboard():
	listings = Item.query.filter_by(lister=current_user)
	return render_template('dashboard.html', name=current_user.name, listings=listings)

@main.route('/search')
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.home'))

	page = request.args.get('page', 1, type=int)
	listings, total = Item.search(g.search_form.q.data, page,
								current_app.config['POSTS_PER_PAGE'])
	next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
		if total > page * current_app.config['POSTS_PER_PAGE'] else None
	prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
		if page > 1 else None
	return render_template('search.html', listings=listings, next_url=next_url, 
		prev_url=prev_url, location=current_app.config['S3_LOCATION'])