from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from app import bcrypt, db
from app.forms.admin.admin import AdminLoginForm, AdminRegisterForm
from app.models.admin.admin import Admin

admin_auth_bp = Blueprint("admin_auth", __name__, url_prefix="/admin")


@admin_auth_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        from flask_login import logout_user

        logout_user()  # Clear any previous session
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and bcrypt.check_password_hash(
            admin.password_hash, form.password.data
        ):
            login_user(admin)
            session["user_type"] = "admin"
            flash("Admin logged in successfully!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid admin username or password.", "danger")
    return render_template("admin/admin_login.html", form=form)


@admin_auth_bp.route("/register", methods=["GET", "POST"])
def admin_register():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        existing_admin = Admin.query.filter(
            (Admin.username == form.username.data) | (Admin.email == form.email.data)
        ).first()
        if existing_admin:
            flash("Username or email already exists.", "danger")
            return render_template("admin/admin_register.html", form=form)
        if not form.password.data:
            flash("Password cannot be empty.", "danger")
            return render_template("admin/admin_register.html", form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        admin = Admin()
        admin.username = form.username.data
        admin.email = form.email.data
        admin.password_hash = hashed_password
        db.session.add(admin)
        db.session.commit()
        flash("Admin account created! You can now log in.", "success")
        return redirect(url_for("admin_auth.admin_login"))
    return render_template("admin/admin_register.html", form=form)


@admin_auth_bp.route("/logout")
@login_required
def admin_logout():
    logout_user()
    flash("Admin logged out.", "success")
    return redirect(url_for("admin_auth.admin_login"))
