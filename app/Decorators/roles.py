from functools import wraps
from flask import g
from app.Util.response import error_res

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if not g.current_user:
                return error_res("Not unauthenticated ", 401)
            valid = [role.name for role in g.current_user.roles]
            if not any(valid):
                return error_res("user doesn't have valid role ", 403)
            return f(*args **kwargs)
        return decorator
    return wrapper
