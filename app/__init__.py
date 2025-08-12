import os
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from urllib.parse import quote_plus
from config import Config

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # type: ignore
login_manager.login_message_category = 'info'
mail = Mail()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)

    # Load default config
    app.config.from_object(Config)

    # Override with env vars (secret key, db credentials)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', app.config.get('SECRET_KEY'))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_DB = os.getenv("MYSQL_DB")

    password_encoded = quote_plus(str(MYSQL_PASSWORD))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_USER}:{password_encoded}@{MYSQL_HOST}/{MYSQL_DB}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask-Mail config from environment
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    # Import blueprints from routes/__init__.py
    from app.routes import auth_bp, calculator_bp, main_bp, guess_bp

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(calculator_bp, url_prefix='/calculator')
    app.register_blueprint(guess_bp, url_prefix='/guess')

    return app

# User loader for Flask-Login
from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
