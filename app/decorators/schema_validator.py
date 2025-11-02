'''from functools import wraps
from flask import request
from pydantic import ValidationError, create_model
from typing import Union, Optional
from app.Models.datatype import Datatype


def sqlalchemy_to_pydantic(sa_model, partial: bool = False):
    """
    Convert a SQLAlchemy model into a dynamic Pydantic model.
    - partial=True → all fields optional (useful for PUT/PATCH)
    - Supports JSON fields (list/dict)
    - Includes bitflag booleans dynamically
    """
    fields = {}

    for column in sa_model.__table__.columns:
        name = column.name

        if name in ("id", "time_created"):
            continue

        field_type = column.type.python_type

        # Handle default values
        default = None
        if column.default is not None and hasattr(column.default, "arg"):
            default_val = column.default.arg
            if not callable(default_val):
                default = default_val

        # JSON → Union[dict, list]
        if str(column.type).lower() == "json":
            field_type = Union[dict, list]

        # Optional for nullable or partial updates
        if column.nullable or partial:
            field_type = Optional[field_type]

        # Field required unless partial
        fields[name] = (
            field_type,
            default if default is not None else (None if partial else ...)
        )

    # Add flags dynamically
    for flag_name, flag_default in Datatype.flags_map.items():
        fields[flag_name] = (Optional[bool], flag_default if not partial else None)

    # Dynamically create a Pydantic model
    return create_model(sa_model.__name__ + "Schema", **fields)


def validate_schema(sa_model, **schema_args):
    """
    Flask decorator that validates incoming JSON using a dynamic Pydantic model.
    Example:
        @validate_schema(Datatype, partial=True)
    Automatically attaches validated data to `request.validated_data`.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            pydantic_model = sqlalchemy_to_pydantic(sa_model, **schema_args)
            data = request.get_json() or {}

            try:
                validated_data = pydantic_model(**data)
            except ValidationError as e:
                return {"success": False, "errors": e.errors()}, 422

            request.validated_data = validated_data.model_dump()
            return f(*args, **kwargs)
        return wrapper
    return decorator
'''