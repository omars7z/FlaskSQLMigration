from functools import wraps
from flask import request
from .response import error_res, suc_res

# datatype_schema = {
#     "datatypename": int,
#     "canDoMathOperation": bool,
#     "canDoLogicalOperation": bool,
#     "isIterable": bool
# }


def validate_json(schema:dict = None):
    
    schema = schema or {}
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs): #accept any combination of arguments (positional(1, 2, 3) + keyword {'a': 1, 'b': 2}
            dt = request.json()
            if not dt:
                return error_res("invalid JSON", 400)
            
            errors = []
            
            for field, field_type in schema.items():
                if field not in dt:
                    errors.append(f"no field added to {field}")
                if field_type == bool and isinstance(field, str):
                    if field.lower() == "true":
                        dt[field] = True
                    elif field.lower() == "false":
                        dt[field] = False
                    else:
                        return error_res(f"Field '{field}' must be a boolean", 400)
                else:
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