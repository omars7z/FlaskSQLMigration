from functools import wraps
from flask import request
from marshmallow import Schema, ValidationError
from app.Util.response import error_res
from typing import Type


def validate_schema(schema_class: Type[Schema]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                return error_res("No data provided", 400)

            schema = schema_class()

            try:
                validated_data = schema.load(data)
                request.validated_data = validated_data
            except ValidationError as err:
                return error_res({
                    "message": "Validation failed",
                    "errors": err.messages
                }, 422)

            return f(*args, **kwargs)
        return wrapper
    return decorator