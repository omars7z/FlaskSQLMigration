from functools import wraps
from flask import g, request, current_app, make_response
from app.Util.cookies import set_access_cookie
from app.Util.response import error_res
from app.Util.jwt_token import (
    decode_access_token, 
    create_access_token,
    get_token_expiry
)
from datetime import datetime, timedelta, timezone

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        access_token = request.cookies.get('access_token')

        payload = decode_access_token(access_token)        
        if not payload:
            return error_res("Invalid or expired token", 401)
        
        g.current_user_id = payload["user_id"]
        g.current_roles = payload.get("roles", [])
        g.current_permissions = payload.get("permissions", [])
        g.current_flags = payload.get("flags", {})
        
        exp_timestamp = get_token_expiry(access_token)
        should_extend = False
        
        if exp_timestamp:
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            time_remaining = exp_datetime - datetime.now(timezone.utc)
            
            if time_remaining < timedelta(minutes=1):
                should_extend = True
        
        response = f(*args, **kwargs)
        
        # if EXTENSION, create new token and update cookie
        if should_extend:
            new_access_token = create_access_token(payload)
            response = make_response(response)
            set_access_cookie(response, new_access_token)
        
        return response
    
    return wrapper