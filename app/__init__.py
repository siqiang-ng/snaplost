from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from elasticsearch import Elasticsearch
import os
import boto3

db = SQLAlchemy()
mail = Mail()

from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mail = Mail(app)

    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'danger'
    login_manager.init_app(app)
    
    from .models import User, Item
    
    @login_manager.user_loader # A user loader tells Flask-Login how to find a specifc user from the ID
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .item import item as item_blueprint
    app.register_blueprint(item_blueprint)


    return app
            
if "__name__" == "__main__":
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)
