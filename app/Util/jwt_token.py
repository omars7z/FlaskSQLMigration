import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app


def _generate_token(payload, secret_key):
    return jwt.encode(payload, secret_key, algorithm="HS256")

def _decode_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])

        if payload.get("expiry") < int(datetime.now(timezone.utc).timestamp()):
            return None
        return payload

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def create_access_token(user):
    payload = {
        "user_id": user.id,
        "user_email": user.email,
        "expiry": int((datetime.now(timezone.utc) + timedelta(hours=2)).timestamp())
    }
    return _generate_token(payload, current_app.config["SECRET_KEY"])


def create_refresh_token(user, days=1):
    payload = {
        "user_id": user.id,
        "expiry": int((datetime.now(timezone.utc) + timedelta(days=days)).timestamp())
    }
    return _generate_token(payload, current_app.config["SECRET_REFRESH_KEY"])


def decode_access_token(token):
    payload = _decode_token(token, current_app.config["SECRET_KEY"])
    return payload["user_id"] if payload else None


def decode_refresh_token(token):
    payload = _decode_token(token, current_app.config["SECRET_REFRESH_KEY"])
    return payload["user_id"] if payload else None
