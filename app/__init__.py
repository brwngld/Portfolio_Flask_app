import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask, app
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # type: ignore
login_manager.login_message_category = "info"
mail = Mail()
limiter = Limiter(key_func=get_remote_address)


def create_app():
    app = Flask(__name__)

    # Load default config
    app.config.from_object(Config)

    # Override with env vars (secret key, db credentials)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", app.config.get("SECRET_KEY"))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_DB = os.getenv("MYSQL_DB")

    password_encoded = quote_plus(str(MYSQL_PASSWORD))
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{MYSQL_USER}:{password_encoded}@{MYSQL_HOST}/{MYSQL_DB}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Flask-Migrate
    migrate = Migrate(app, db)

    # Flask-Mail config from environment
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    # Import blueprints from routes/__init__.py
    from app.routes import auth_bp, calculator_bp, guess_bp, main_bp
    from app.routes.admin.auth import admin_auth_bp
    from app.routes.admin.dashboard import admin_bp

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(calculator_bp, url_prefix="/calculator")
    app.register_blueprint(guess_bp, url_prefix="/guess")
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_auth_bp)

    return app


from app.models.admin.admin import Admin
# User loader for Flask-Login
from app.models.user import User


@login_manager.user_loader
def load_user(user_id):
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin
    user = User.query.get(int(user_id))
    return user
