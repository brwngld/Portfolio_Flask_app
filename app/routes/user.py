from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app import bcrypt, db
from app.forms import RegisterForm
from app.models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    from flask_wtf import FlaskForm
    from wtforms import PasswordField, StringField, SubmitField
    from wtforms.validators import DataRequired

    class LoginForm(FlaskForm):
        username = StringField("Username", validators=[DataRequired()])
        password = PasswordField("Password", validators=[DataRequired()])
        submit = SubmitField("Login")

    form = LoginForm()
    current_year = datetime.now().year
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        from app import bcrypt

        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            if getattr(user, "is_admin", False):
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("main.index"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form, current_year=current_year)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    current_year = datetime.now().year
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if existing_user:
            flash("Username or email already exists. Please choose another.", "danger")
            return render_template(
                "register.html", form=form, current_year=current_year
            )

        # Create new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
    user = User()
    user.username = form.username.data
    user.email = form.email.data
    user.password_hash = hashed_password
    user.first_name = ""
    user.last_name = ""
    user.number = ""
    user.country = ""
    user.state = ""
    user.city = ""
    user.address = ""
    user.is_approved = True
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created for {form.username.data}! You can now log in.", "success"
        )
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form, current_year=current_year)
