from functools import wraps 
from flask import request 
from .response import error_res
import re
#if body has error return bad request 

def validate_post(flags_map: dict = None):
    flags_map = flags_map or {}

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                return error_res("invalid JSON", 400)

            # fill missing flags with defaults
            validated_data = {**flags_map, **data}

            example = validated_data.get("example")
            if not example:
                return error_res("Missing 'example' in request body", 400)

            examples = example if isinstance(example, list) else [example]
            txts = [v.lower() for e in examples for v in e.values()]

            errors = []

            # map flags and example 
            flag_checks = {
                "canDoMathOperation": r"[\+\-\*/\^%]",
                "canDoLogicalOperation": r"\b(and|or|not|&|\|)\b",
                "isIterable": r"\b(for|while|loop|iter|range)\b"
            }

            for flag, pattern in flag_checks.items():
                flag_val = validated_data.get(flag, False)
                matching_pattern = any(re.search(pattern, str(txt)) for txt in txts)
                
                if flag_val and not matching_pattern:        
                    errors.append(f"{flag} is True but example doesn't contain content")
                if matching_pattern and not flag_val:
                    errors.append(f"{flag} is Not found but there is an Example for it")

            if errors:
                return error_res({"message": "Example content inconsistent with flags", "details": errors}, 400)

            return f(*args, **kwargs)
        return wrapper
    return decorator
