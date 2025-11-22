from functools import wraps
from flask import g
from app.Util.response import error_res

def superadmin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        flags = getattr(g, "current_flags", g.get("current_flags", {}))
        if not flags.get("isSuperAdmin"):
            return error_res("Permission denied: Super admin only", 403)
        return f(*args, **kwargs)
    return decorated
