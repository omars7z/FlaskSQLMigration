
import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

idle = 5

def create_access_token(user_id, idle):
    payload = {
        "user_id" : user_id,
        "expiry" : int((datetime.now(timezone.utc) + timedelta(minutes=idle)).timestamp()) #datetime(2025, 11, 3, 8, 0, 0 + timezone.utc+10mins) -> timestamp(float) -> int
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
        
'''
Built it decorator that 
@jwt_required()
def get(self):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return suc_res({"user": user.name})
    
Reads the Authorization header (Bearer <token>)
Validates the signature and expiry
Handles errors with proper JSON responses
Lets you define custom callbacks (e.g. user lookup, role check)

can be put in custom decorator
@active_user_required
def get(self):
    return suc_res({"user": g.current_user.name})
    '''