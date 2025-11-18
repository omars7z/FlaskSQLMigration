from functools import wraps
from flask import g, request
from app.Util.response import error_res
from app.Util.jwt_token import decode_refresh_token
from app.Models.user import User

def refresh_jwt(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return error_res("Missing or wrong auth header", 401)

        refresh_token = auth_header.split(" ")[1]

        user_id = decode_refresh_token(refresh_token)
        if not user_id:
            return error_res("Invalid or expired refresh token", 401)

        user = User.query.get(user_id)
        if not user or not user.to_dict_flags().get("isActive"):
            return error_res("Wrong user or inactive", 401)

        g.current_user = user

        return f(*args, **kwargs)
    
    return wrapper
