from functools import wraps
from flask import request
from ..Util.response import error_res
from app.Models.datatype import Datatype
import re

def validate_post():
    """
    Validator for POST/PUT request JSON using the Datatype model.
    Pulls name max length and flags dynamically from Datatype.
    """

    name_column = Datatype.__table__.columns["name"]
    max_length = getattr(name_column.type, "length", None)
    flag_checks = {
        "canDoMathOperation": r"[\+\-\*/\^%]",
        "canDoLogicalOperation": r"\b(and|or|not|&|\|)\b",
        "isIterable": r"\b(for|while|loop|iter|range)\b"
    }

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json() or {}
            errors = []

            name = data.get("name")
            if name and max_length and len(str(name)) > max_length:
                errors.append(f"Field 'name' must not exceed {max_length} characters")

            # Flatten example
            example = data.get("example", [])
            if not isinstance(example, list):
                example = [example]

            txts = []
            for e in example:
                if isinstance(e, dict):
                    txts.extend(str(v).lower() for v in e.values())


            # --- Validate flags logically ---
            for flag, pattern in flag_checks.items():
                flag_val = data.get(flag, False)
                matching_pattern = any(re.search(pattern, str(txt)) for txt in txts)

                if flag_val and not matching_pattern:
                    errors.append(f"{flag} is True but example doesn't contain content")
                if matching_pattern and not flag_val:
                    errors.append(f"{flag} is Not found but there is an Example for it")

            if errors:
                return error_res({"message": "Validation errors", "details": errors}, 400)

            return f(*args, **kwargs)

        return wrapper
    return decorator
