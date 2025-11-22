import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

def create_access_token(user):
    if isinstance(user, int):   
        user = current_app.user_service.get_by_id(user) #change to current_app.config["user_id"]

    expire = datetime.now(timezone.utc) + current_app.config["JWT_TOKEN_TIME"]    
    
    permissions = user.get_permissions()
    permissions_list = [{"resource":perm.resource, "action":perm.action} for perm in permissions]
    roles = [role.name for role in user.roles]
    flags = user.to_dict_flags()
    
    payload = {
        "user_id": user.id,
        "role" : roles,
        "permissions" : permissions_list,
        "flags":flags,
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }
    
    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return token

def decode_access_token(token):
    """Decode and validate access token"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_token_expiry(token):
    payload = jwt.decode(
        token,
        current_app.config['SECRET_KEY'],
        algorithms=["HS256"],
        options={"verify_exp": False}
    )
    return payload.get("exp")