from flask import Blueprint, render_template, redirect, flash, request, url_for, current_app, send_from_directory
from flask_login import login_required, current_user
from app.models import Item, User
from app import db
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app.resources import get_client, delete_obj

item = Blueprint('item', __name__)


@item.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    user = User.query.get(current_user.id)
    s3 = get_client()

    if request.method == 'POST':
        category = request.form.get('category')
        item = request.form['item']
        description = request.form['description']
        occurdate = request.form['occurdate']
        takentime = request.form['time']
        number = request.form['number']
        photo = request.files['photo']

        if not category:
            flash('Category of the listing is required!', 'warning')
            return render_template('create.html')
        if not item:
            flash('Item name is required!', 'warning')
            return render_template('create.html')
        if not description:
            flash('Item description is required!', 'warning')
            return render_template('create.html')
        if not occurdate:
            flash('Date is required!', 'warning')
            return render_template('create.html')
        if not takentime:
            flash('Time is required!', 'warning')
            return render_template('create.html')
        else:
            conDate = datetime.strptime(occurdate, '%Y-%m-%d')
            conTime = datetime.strptime(takentime, "%H:%M").time()

            if photo: 
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))

                with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
                    s3.upload_file(Bucket='snaplostesq', Filename=f.name, Key=filename,
                    ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": photo.content_type
                })

            else: 
                filename = ""

            new_item = Item(category=category, item=item, description=description, 
                occurdate=conDate, time=conTime, number=number, photo=filename, lister=user)

            db.session.add(new_item)
            db.session.commit()
            flash('"{}" is successfully listed!'.format(item), 'info')
            return redirect(url_for('main.home'))

    return render_template('create.html')

@item.route('/<int:item_id>/edit', methods=('GET','POST'))
@login_required
def edit(item_id):
    item = Item.query.filter_by(id=item_id).first()
    user = User.query.get(current_user.id)
    s3 = get_client()

    if request.method == 'POST':
        category = request.form.get('category')
        name = request.form['item']
        description = request.form['description']
        occurdate = request.form['occurdate']
        takentime = request.form['time']
        number = request.form['number']
        photo = request.files['photo']

        if not category:
            flash('Category of the listing is required!', 'warning')
            return render_template('edit.html', item=item)
        if not name:
            flash('Item name is required!', 'warning')
            return render_template('edit.html', item=item)
        if not description:
            flash('Item description is required!', 'warning')
            return render_template('edit.html', item=item)
        if not occurdate:
            flash('Date is required!', 'warning')
            return render_template('edit.html', item=item)
        if not takentime:
            flash('Time is required!'), 'warning'
            return render_template('edit.html', item=item)
        else:
            conDate = datetime.strptime(occurdate, '%Y-%m-%d')
            conTime = datetime.strptime(takentime, "%H:%M:%S").time()

            filename = secure_filename(photo.filename)

            updated = Item.query.get(item_id)
            if (category != updated.category):
                updated.category = category
            if (name != updated.item):
                updated.item = name
            if (description != updated.description):
                updated.description = description
            if (conDate != updated.occurdate):
                updated.occurdate = conDate
            if (conTime != updated.time):
                updated.time = conTime
            if (number != updated.number):
                updated.number = number
            if (filename != updated.photo):

                if photo: #if there is a photo uploaded
                    if updated.photo: #if there is already one uploaded photo, remove it.
                        delete_obj(updated.photo)

                    photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))
                    updated.photo = filename

                    with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
                        s3.upload_file(Bucket='snaplostesq', Filename=f.name, Key=filename,
                        ExtraArgs={
                        "ACL": "public-read",
                        "ContentType": photo.content_type
                    })

            db.session.commit()
            flash('"{}" is successfully edited!'.format(name), 'info')
            return redirect(url_for('main.home'))

    else:
        return render_template('edit.html', item=item)


@item.route('/<int:listing_id>')
def listing(listing_id):
    listing = Item.query.filter_by(id=listing_id).first()
    location = current_app.config['S3_LOCATION']
    return render_template('listing.html', listing=listing, location=location)


@item.route('/<int:item_id>/delete', methods=('POST',))
@login_required
def delete(item_id):
    item = Item.query.filter_by(id=item_id).first()

    ditem = Item.query.get(item_id)
    db.session.delete(ditem)
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(item.item), 'info')
    return redirect(url_for('main.home'))
