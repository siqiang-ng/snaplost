from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True} 
    
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Item(UserMixin, db.Model):
    __tablename__ = "item"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    occurdate = db.Column(db.Date)
    time = db.Column(db.Time)


