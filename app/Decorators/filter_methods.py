from functools import wraps
from flask import request
from app.Util.response import error_res

#add filtering by relational tables (foreing keys, columns...)

def auto_filter_method(model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            filters = {}
            query = model.query
            args_dict = request.args.to_dict()
            
            for key, val in list(args_dict.items()):
                if hasattr(model, key):
                    v = getattr(model, key)
                    query = query.filter(v==val)
                    filters[key] = val
                    
                elif hasattr(model, "flags") and key in model.flags:
                        filters[key] = val.lower() == "true"
                else:
                    return error_res(f"invalide params: {key}", 400)
                
            kwargs['filters'] = filters
            return func(*args, **kwargs)
                    
        return wrapper
    return decorator
                    