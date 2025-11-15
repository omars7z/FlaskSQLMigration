from functools import wraps
from flask import g
from app.Util.response import error_res

def access_required(resource: str=None , action: str=None , roles: list[str]= None):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            user = g.current_user
            if not user:
                return error_res("Not unauthenticated ", 401)
            
            user_role_name = [role.name for role in user.roles]  #if role (that has permission)
            if roles and any(r in user_role_name for r in roles):
                return f(*args **kwargs)
        
            if resource and action:
                user_permissions = user.get_permissions()
            
            valid = any(
                perm.resource==resource and perm.action==action
                for perm in user_permissions
                )
            if valid:
                return f(*args, **kwargs)
            
            return error_res("user doesn't have permission to this action ", 403)
        return decorator
    return wrapper

