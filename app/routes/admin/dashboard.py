from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import bcrypt, db
from app.models.admin.admin import Admin
from app.models.user import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# Protect all admin routes: only allow access for admin users
@admin_bp.before_request
def restrict_to_admin():
    if not current_user.is_authenticated or not isinstance(
        current_user._get_current_object(), Admin
    ):
        flash("Admin access required.", "danger")
        return redirect(url_for("admin_auth.admin_login"))


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    users = User.query.all()
    return render_template("admin/dashboard.html", users=users)


@admin_bp.route("/user/<int:user_id>")
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("admin/user_profile.html", user=user)


@admin_bp.route("/user/<int:user_id>/approve", methods=["POST"])
@login_required
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash("User approved.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/user/<int:user_id>/change_password", methods=["POST"])
@login_required
def change_password(user_id):
    user = User.query.get_or_404(user_id)
    new_password = request.form.get("new_password")
    if new_password:
        user.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
        db.session.commit()
        flash("Password changed successfully.", "success")
    else:
        flash("Password cannot be empty.", "danger")
    return redirect(url_for("admin.user_profile", user_id=user_id))


@admin_bp.route("/user/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for("admin.dashboard"))
