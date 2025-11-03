from jwt import JWT, exceptions
from datetime import datetime, timedelta, timezone
from flask import current_app

def create_access_token(user_id):
    payload = {
        "user_id" : user_id,
        "expiry" : datetime.now(timezone.utc) + timedelta(minutes=10)
    }
    
    token = JWT.encode(payload, current_app["SECRET_KEY"], algorithm="HS256") #header.payload.signature
    return token

def decode_access_token(token):
    try:
        payload = JWT.decode(token, current_app["SECRET_KEY"], algorithm="HS256")
        return payload["current_id"]
    except JWT.ExpiredSignatureError:
        return None
    except exceptions.InvalidKeyTypeError:
        return None