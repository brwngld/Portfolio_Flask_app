from datetime import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    """
    Represents a registered user in the application.
    Includes authentication, profile details, and creation timestamp.
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(180), nullable=False)
    number = db.Column(db.String(80), nullable=True)
    country = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

    # Password logic handled in route, not in model
