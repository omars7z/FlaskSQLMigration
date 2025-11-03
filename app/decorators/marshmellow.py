# app/decorators/marshmallow_schema.py
from functools import wraps
from flask import request
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import marshmallow
from marshmallow import fields, ValidationError, INCLUDE
from typing import Type
from app.extensions import db

def sqlalchemy_to_marshmallow(sa_model: Type, partial: bool = False, session=None):
    """
    Dynamically create a Marshmallow schema from a SQLAlchemy model.
    - partial=True → allows partial updates
    - session → SQLAlchemy session required if load_instance=True
    - Automatically includes Datatype flags as optional boolean fields
    """
    class DynamicSchema(SQLAlchemyAutoSchema):
        class Meta:
            model = sa_model
            load_instance = True #make orm objecct to insert directly
            sqla_session = session or db.session
            include_fk = True
            unknown = marshmallow.INCLUDE

    # Add dynamic JSON fields and bitflags
    for column in sa_model.__table__.columns:
        if str(column.type).lower() == "json":
            setattr(DynamicSchema, column.name, 
                    fields.Dict(keys=fields.Str(), 
                                values=fields.Raw(), 
                                required=not partial))#keys r string, values r any, partial for put method

    if hasattr(sa_model, "flags_map"):
        for flag_name in sa_model.flags_map.keys():
            setattr(DynamicSchema, flag_name, fields.Boolean(required=False))

    return DynamicSchema


def validate_schema(sa_model: Type, partial: bool = False):
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json() or {}
            SchemaClass = sqlalchemy_to_marshmallow(sa_model, partial=partial, session=db.session)
            schema = SchemaClass()

            try:
                validated_obj = schema.load(data)
            except ValidationError as err:
                return {"success": False, "errors": err.messages}, 422

            request.validated_data = validated_obj
            return f(*args, **kwargs)
        return wrapper
    return decorator
