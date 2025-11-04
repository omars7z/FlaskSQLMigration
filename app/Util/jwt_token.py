
import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app


def create_access_token(user_id):
    payload = {
        "user_id" : user_id,
        "expiry" : int((datetime.now(timezone.utc) + timedelta(minutes=5)).timestamp()) #datetime(2025, 11, 3, 8, 0, 0 + timezone.utc+10mins) -> timestamp(float) -> int
    }
    
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256") #header.payload.signature
    return token

def decode_access_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]  
            )
            if payload["expiry"] < int(datetime.now(timezone.utc).timestamp()):
                return None
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None