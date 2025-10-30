from functools import wraps
from flask import request
from .response import error_res

def validate_types(flags_map: dict = None):
    """Validate boolean fields and name length in request JSON."""
    flags_map = flags_map or {}

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                return error_res("Invalid JSON", 400)

            errors = []

            # Ensure all flags are booleans
            for field, default in flags_map.items():
                val = data.get(field, default)
                if isinstance(val, str):
                    val_lower = val.lower()
                    if val_lower == "true":
                        data[field] = True
                    elif val_lower == "false":
                        data[field] = False
                    else:
                        errors.append(f"Field '{field}' must be a boolean")
                elif not isinstance(val, bool):
                    errors.append(f"Field '{field}' must be a boolean")
                else:
                    data[field] = val

            # validate name length
            name = data.get("name")
            if name and len(str(name)) > 30:
                errors.append("Field 'name' must not exceed 30 characters")

            if errors:
                return error_res("; ".join(errors), 400)

            return f(*args, **kwargs)

        return wrapper
    return decorator
