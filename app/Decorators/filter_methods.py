from functools import wraps
from flask import request
from app.Util.response import error_res

#add filtering by relational tables (foreing keys, columns...)

def auto_filter_method(model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            filters = {}

            raw_filters = request.args.get("filters", "")
            if raw_filters:

                
                if "," in raw_filters:
                    pairs = raw_filters.split(",")
                else:
                    pairs = raw_filters.split("&")

                for pair in pairs:
                    if "=" not in pair:
                        return error_res(f"Invalid filter format: {pair}", 400)

                    key, val = pair.split("=", 1)
                    key = key.strip()
                    val = val.strip()

                    if hasattr(model, key):
                        filters[key] = val
                    else:
                        return error_res(f"Invalid filter field: {key}", 400)

            kwargs["filters"] = filters
            return func(*args, **kwargs)
        return wrapper
    return decorator
