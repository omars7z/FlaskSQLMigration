from functools import wraps
from flask import request
from app.Util.response import error_res

def auto_filter_method(model):
    def decorator(func):
        @wraps(func)
        def wrapper(resource, *args, **kwargs):
            
            filters = {}
            query = model.query
            args_dict = request.args.to_dict()
            
            for key, val in list(args_dict.items()):
                if hasattr(model, key):
                    query = query.filter(getattr(model, key)==val)
                    filters[key] = val
                    
                elif key in model.flags_map:
                        filters[key] = val.lower() == "true"
                else:
                    return error_res(f"invalide params {key}", 400)
                
                
            return func(resource, filters, *args, **kwargs)
                    
        return wrapper
    return decorator
                    