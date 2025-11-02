import jwt
from datetime import datetime, timedelta
from flask import current_app

def create_access_token(user_id):
    header = {
        "user_id" : user_id,
        "expiry" : datetime.now(datetime.timezone.utc) + timedelta(minutes=10)
    }
    
    return jwt.JWT.encode(header, current_app["SECRET_KEY"], algorithm="HS256") #header.payload.signature

def decode_access_token(token):
    try:
        payload = jwt.JWT.decode(token, current_app["SECRET_KEY"], algorithm="HS256")
        return payload["current_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None