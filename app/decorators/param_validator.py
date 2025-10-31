
from functools import wraps
from flask import request
from app.util.response import error_res

def require_query_param(param_name, param_type=None):
    """Decorator to require a query parameter in the request."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            value = request.args.get(param_name, type=param_type)
            if value is None:
                return error_res(f"Missing '{param_name}'", 400)
            # Store the value as a temporary attribute on self
            setattr(self, f"_{param_name}", value)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
