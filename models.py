from . import db

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True} 
    
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Item(db.Model):
    __tablename__ = "item"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    occurdate = db.Column(db.Date)
    time = db.Column(db.Time)
    photo = db.Column(db.LargeBinary)

