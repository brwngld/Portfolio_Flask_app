from .auth import admin_auth_bp, admin_login, admin_register
from .dashboard import (admin_bp, approve_user, change_password, dashboard,
                        debug_users, dismiss_admin, restrict_to_admin,
                        user_profile)

__all__ = [
    "admin_auth_bp",
    "admin_login",
    "admin_register",
    "admin_bp",
    "approve_user",
    "change_password",
    "dashboard",
    "restrict_to_admin",
    "user_profile",
    "dismiss_admin",
    "debug_users",
]
