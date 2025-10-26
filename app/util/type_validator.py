from functools import wraps
from flask import request
from .response import error_res, suc_res

#if body has error return bad request 


def validate_types(flags_map:dict = None):
    
    flags_map = flags_map or {}
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs): #accept any combination of arguments (positional(1, 2, 3) + keyword {'a': 1, 'b': 2}
            dt = request.get_json()
            if not dt:
                return error_res("invalid JSON", 400)
            
            errors = []
            
            for field, default_field in flags_map.items():
                field_type = bool
                if field not in dt:
                    errors.append(f"no field added to {field}")
                    continue
                if isinstance(dt[field], str):
                    val = dt[field].lower()
                    if val == "true":
                        dt[field] = True
                    elif val == "false":
                        dt[field] = False
                    else:
                        error_res(f"Field '{field}' must be a boolean", 400)
                        continue
                
                if not isinstance(dt[field], field_type):
                    errors.append(f"field {field} is wrong datatype, it shoudl be {field_type.__name__}")
                    
            
            if "name" in dt and len(str(dt["name"]))>50:
                errors.append("Field 'name' must not exceed 50 characters")
            
            if errors:
                return error_res("; ".join(errors), 400)

            kwargs["dt"] = dt
            return f(*args, **kwargs)
        return wrapper
    return decorator