from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import SignupForm, ResetPasswordRequestForm, ResetPasswordForm
from .emails import send_password_reset_email
from .models import User, Item
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = SignupForm()

	if form.validate_on_submit():
		user = User(name=form.name.data, email=form.email.data, 
			password=generate_password_hash(form.password.data))
		db.session.add(user)
		db.session.commit()
		flash('Account has been successfully created!', 'success')
		return redirect(url_for('auth.login'))

	return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	session.pop('email', None) # Remove 'email' from the session if it exists
	return redirect(url_for('main.home'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    session['email'] = email # Save in session
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('auth.login'))
	
    login_user(user, remember=remember)
    return redirect(url_for('main.dashboard'))

@auth.route('/settings', methods =['GET', 'POST'])
@login_required
def settings():
	if request.method == 'POST':
		newname = request.form.get('name') 
		oldpw = request.form.get('oldpw')
		newpw = request.form.get('newpw')

		updated = User.query.get(current_user.id)
		if (newname != updated.name):
			updated.name = newname
		
		if oldpw:
			if newpw:
				if check_password_hash(updated.password, oldpw):
					updated.password = generate_password_hash(newpw)
				else:
					flash('Invalid password!', 'danger')
					return render_template('settings.html', name=current_user.name)
			else:
				flash('Fill in your new password!', 'danger')
				return render_template('settings.html', name=current_user.name)

		if newpw:
			if not oldpw:
				flash('Fill in your old password!', 'danger')
				return render_template('settings.html', name=current_user.name)

		db.session.commit()
		flash('Changes have been saved successfully!', 'success')
		return redirect(url_for('main.home'))
	
	else:
		return render_template('settings.html', name=current_user.name)

@auth.route('/deleteAcc', methods=['POST'])
@login_required
def deleteAcc():    
	duser = User.query.get(current_user.id)

	db.session.delete(duser)
	db.session.commit()
	flash('"{}" was successfully deleted!'.format(current_user.name), 'success')
	return redirect(url_for('main.home'))

@auth.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('Check your email for the instructions to reset your password', 'warning')
		return redirect(url_for('auth.login'))
	return render_template('reset_password_request.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('main.home'))

	form = ResetPasswordForm()
	if form.validate_on_submit():
		newpw = form.password.data
		user.password = generate_password_hash(newpw)
		db.session.commit()
		flash('Your password has been reset.', 'success')
		return redirect(url_for('auth.login'))

	return render_template('reset_password.html', form=form)