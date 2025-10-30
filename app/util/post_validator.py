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

            # Fill missing flags with defaults
            validated_data = {**flags_map, **data}

            example = validated_data.get("example")
            if not example:
                return error_res("Missing 'example' in request body", 400)

            examples = example if isinstance(example, list) else [example]

            txt = " ".join(str(v).lower() for e in examples for v in e.values())

            errors = []

            # Check consistency between flags and example content
            flag_checks = {
                "canDoMathOperation": r"[\+\-\*/\^%]",
                "canDoLogicalOperation": r"\b(and|or|not|&|\|)\b",
                "isIterable": r"\b(for|while|loop|iter|range)\b"
            }

            relevant_flags = []

            for flag, pattern in flag_checks.items():
                if validated_data.get(flag):
                    if not re.search(pattern, txt):
                        errors.append(f"{flag} is True but example doesn't contain relevant content")
                    else:
                        relevant_flags.append(flag)

            if examples and not relevant_flags:
                errors.append("Example exists but no relevant flags match its content")

            if errors:
                return error_res({"message": "Example content inconsistent with flags", "details": errors}, 400)

            return f(*args, **kwargs)

        return wrapper
    return decorator
