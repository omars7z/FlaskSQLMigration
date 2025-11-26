import redis
from flask import current_app

_redis_instance = None

#singlton instance
def get_redis_connection():
    global _redis_instance
    if _redis_instance:
        return _redis_instance

    host = current_app.config.get("REDIS_HOST", "127.0.0.1")
    port = current_app.config.get("REDIS_PORT", 6379)
    db = current_app.config.get("REDIS_DB", 0)

    _redis_instance = redis.Redis(
        host=host,
        port=port,
        db=db,
        decode_responses=True
    )
    try:
        _redis_instance.ping()
    except redis.ConnectionError as e:
        raise ConnectionError(f"Cannot connect to Redis at {host}:{port} -> {e}")

    return _redis_instance
