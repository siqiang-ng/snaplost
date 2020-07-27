import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	POSTS_PER_PAGE = 24
	UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static')
	ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
	S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
	S3_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
	S3_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")
	S3_LOCATION = "https://{}.s3-ap-southeast-1.amazonaws.com/".format(S3_BUCKET)