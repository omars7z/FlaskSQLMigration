from functools import wraps
from flask import request
from app.util.response import error_res
from app.models.datatype import Datatype

def auto_filter_method(model):
    def decorator(func):
        @wraps(func)
        def wrapper(resource, *args, **kwargs):
            
            filters = {}
            query = model.query
            args_dict = request.args.to_dict()
            
            for key, val in list(args_dict.items()):
                if hasattr(model, key):
                    col = getattr(model, key)
                    query = query.filter(getattr(model, key))
                    py_type = getattr(col.type, 'python_type', str)
                    if py_type == bool:
                        val = val.lower() == "true"
                    else:
                        val = py_type(val)
                    filters[key] = val
                elif key in model.flags_map:
                        filters[key] = val.lower() == "true"
                else:
                    return error_res(f"invalide params {key}", 400)
                
                
            return func(resource, filters, *args, **kwargs)
                    
        return wrapper
    return decorator
                    