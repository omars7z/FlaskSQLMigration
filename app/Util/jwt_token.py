# from jwt import JWT, exceptions
import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app


def create_access_token(user_id):
    payload = {
        "user_id" : user_id,
        "expiry" : (datetime.now(timezone.utc) + timedelta(minutes=10)).timestamp()
    }
    
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256") #header.payload.signature
    return token

def decode_access_token(token):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithm="HS256")
        # return payload["current_id"]
        return payload["user_id"]
    # except (jwt.PyJWK.JWTDecodeError, exceptions.InvalidKeyTypeError):
    except TypeError:
        return None