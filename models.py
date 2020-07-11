from flask_login import UserMixin
from . import db
from time import time
import jwt
from flask import current_app

class User(UserMixin, db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True} 
    
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)
    listing = db.relationship('Item', backref='lister', cascade='all, delete-orphan', lazy='dynamic')

    def get_reset_password_token(self, expires_in=1800):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Item(UserMixin, db.Model):
    __tablename__ = "item"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    occurdate = db.Column(db.Date)
    time = db.Column(db.Time)
    number = db.Column(db.String(100))
    photo = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

