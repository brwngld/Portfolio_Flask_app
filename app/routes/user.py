from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from app import bcrypt, db
from app.forms import ProfileForm, RegisterForm
from app.models.user import User

auth = Blueprint("auth", __name__)


# Profile view and update
@auth.route("/profile", methods=["GET", "POST"], endpoint="profile")
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    current_year = datetime.now().year
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.number = form.number.data
        current_user.country = form.country.data
        current_user.state = form.state.data
        current_user.city = form.city.data
        current_user.address = form.address.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("auth.profile"))
    return render_template("profile.html", form=form, current_year=current_year)


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
        from flask_login import logout_user

        logout_user()  # Clear any previous session
        user = User.query.filter_by(username=form.username.data).first()
        from app import bcrypt

        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            session["user_type"] = "user"
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
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.number = form.number.data
        user.country = form.country.data
        user.state = form.state.data
        user.city = form.city.data
        user.address = form.address.data
        user.is_approved = True
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created for {form.username.data}! You can now log in.", "success"
        )
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form, current_year=current_year)
