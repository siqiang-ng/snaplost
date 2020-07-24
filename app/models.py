from flask_login import UserMixin
from app import db
from time import time
import jwt
from flask import current_app
from app.search import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
	@classmethod
	def search(cls, expression, page, per_page):
		ids, total = query_index(cls.__tablename__, expression, page, per_page)
		if total == 0:
			return cls.query.filter_by(id=0), 0
		when = []
		for i in range(len(ids)):
			when.append((ids[i], i))
		return cls.query.filter(cls.id.in_(ids)).order_by(
			db.case(when, value=cls.id)), total

	@classmethod
	def before_commit(cls, session):
		session._changes = {
			'add': list(session.new),
			'update': list(session.dirty),
			'delete': list(session.deleted)
		}

	@classmethod
	def after_commit(cls, session):
		for obj in session._changes['add']:
			if isinstance(obj, SearchableMixin):
				add_to_index(obj.__tablename__, obj)
		for obj in session._changes['update']:
			if isinstance(obj, SearchableMixin):
				add_to_index(obj.__tablename__, obj)
		for obj in session._changes['delete']:
			if isinstance(obj, SearchableMixin):
				remove_from_index(obj.__tablename__, obj)
		session._changes = None

	@classmethod
	def reindex(cls):
		for obj in cls.query:
			add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


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

class Item(SearchableMixin, db.Model):
	__tablename__ = "item"
	__table_args__ = {'extend_existing': True}
	__searchable__ = ['item', 'description']

	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(100), nullable=False)
	item = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(1000), nullable=False)
	occurdate = db.Column(db.Date)
	time = db.Column(db.Time)
	number = db.Column(db.String(100))
	photo = db.Column(db.String(100))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

