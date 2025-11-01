import jwt
from datetime import datetime, timedelta
from flask import current_app

def create_access_token(self, user_id):
    payload = {
        "user_id" : user_id,
        "expiry" : datetime.now(datetime.timezone.utc) + timedelta(minutes=10)
    }
    
    return jwt.encode(payload, current_app["SECRET_KEY"], algorithm='HS256') #header.payload.signature

