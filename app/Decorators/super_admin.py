
from functools import wraps
from flask import g
from app.Util.response import error_res

def superadmin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = getattr(g, "current_user", None)
        if not current_user:
            return error_res("User not authenticated", 401)

        # Check if user has 'isSuperAdmin' flag
        if not current_user.to_dict_flags().get("isSuperAdmin"):
            return error_res("permission denied: Super admin only", 403)

        return f(*args, **kwargs)
    return decorated

    