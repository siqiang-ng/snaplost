from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email = email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
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
                    updated.password = generate_password_hash(newpw, method='sha256')
                else:
                    flash('Wrong password!')
                    return render_template('settings.html', name=current_user.name)
            else:
                flash('Fill in your new password!')
                return render_template('settings.html', name=current_user.name)

        if newpw:
            if not oldpw:
                flash('Fill in your old password!')
                return render_template('settings.html', name=current_user.name)

        db.session.commit()
        flash('Changes have been saved successfully!')
        return redirect(url_for('main.home'))
    
    else:
        return render_template('settings.html', name=current_user.name)

@auth.route('/deleteAcc', methods=['POST'])
@login_required
def deleteAcc():
    user = User.query.filter_by(id=current_user.id).first()
    
    duser = User.query.get(current_user.id)
    db.session.delete(duser)
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(user.name))
    return redirect(url_for('main.home'))
