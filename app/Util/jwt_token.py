import app.Util.jwt_token as jwt_token
from datetime import datetime, timedelta
from flask import current_app

def create_access_token(user_id):
    header = {
        "user_id" : user_id,
        "expiry" : datetime.now(datetime.timezone.utc) + timedelta(minutes=10)
    }
    
    return jwt_token.encode(header, current_app["SECRET_KEY"], algorithm='HS256') #header.payload.signature

