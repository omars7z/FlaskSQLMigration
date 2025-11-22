from functools import wraps
from flask import g
from app.Util.response import error_res

def access_required(resource: str=None , action: str=None , roles: list[str]= None):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            user = getattr(g, "current_user_id", None)
            user_roles = getattr(g, "current_roles", [])
            user_permissions = getattr(g, "current_permissions", [])
            if not user:
                return error_res("Not unauthenticated ", 401)
            
            if roles and any(r in user_roles for r in roles):
                return f(*args, **kwargs)
        
            if resource and action:
                valid = any(
                perm.get("resource") and perm.get("action")
                for perm in user_permissions
                )
                if valid:
                    return f(*args, **kwargs)
            
            return error_res("user doesn't have permission to this action ", 403)
        return decorator
    return wrapper

