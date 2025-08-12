from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    # login logic here
    current_year = datetime.now().year
    return render_template("login.html", current_year=current_year)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("main.home"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    # registration logic here
    current_year = datetime.now().year
    return render_template("register.html", current_year=current_year)
