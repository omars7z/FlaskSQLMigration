from functools import wraps
from flask import g, request
from app.Config.redis import get_redis_connection
from app.Util.response import error_res

def rate_limit(limit: int, window: int):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = getattr(g, "current_user_id", None) or request.remote_addr
            key = f"rate:{user_id}:{request.endpoint}"

            r = get_redis_connection()
            current = r.get(key)

            if current and int(current) >= limit:
                ttl = r.ttl(key) or window
                return error_res({
                    "error": "Too Many Requests",
                    "retry_after_seconds": ttl
                }, 429)

            pipe = r.pipeline()
            pipe.incr(key)
            pipe.expire(key, window)
            pipe.execute()

            return f(*args, **kwargs)
        return wrapper
    return decorator
