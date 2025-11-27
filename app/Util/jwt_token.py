import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app, g

def user_to_payload(user):
    return {
        "user_id": user.id,
        "roles": [role.name for role in user.roles],
        "permissions": [{"resource": p.resource, "action": p.action} for p in user.get_permissions()],
        "flags": user.to_dict_flags()
    }


def create_access_token(payload_data):
    
    user_id = payload_data.get("user_id")
    roles = payload_data.get("roles", [])
    permissions = payload_data.get("permissions", [])
    flags = payload_data.get("flags", {})
    
    expire = datetime.now(timezone.utc) + current_app.config["JWT_TOKEN_TIME"]
    
    payload = {
        "user_id": user_id,
        "role" : roles,
        "permissions" : permissions,
        "flags":flags,
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }
    print(payload)
    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return token

def decode_access_token(token):
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

