import os 

class Config(object):
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.urandom(24)
	SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USERNAME= 'esqlostesq@gmail.com'
	MAIL_PASSWORD = 'snaplost'
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
