from functools import wraps
from flask import request
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError
from typing import Type
from app.extensions import db

def sqlalchemy_to_marshmallow(sa_model: Type, partial: bool = False, session=None):
    """
    Dynamically create marshmallow schema from a SQLAlchemy model
    - partial=True -> for partial Put
    - session -> SQLAlchemy session required if load_instance=True
    - flags optional fields
    """
    class DynamicSchema(SQLAlchemyAutoSchema):
        class Meta:
            model = sa_model
            load_instance = True #make orm objecct to insert directly
            sqla_session = session or db.session
            include_fk = True

    # add dynamic JSON fields and bitflags
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
                missing_fields = [field for field, msgs in err.messages.items() if any("Missing data" in m for m in msgs)]
                erros = {
                    "message": "Validation failed",
                    "missing_fields": missing_fields,
                    "errors": err.messages,
                }
                return {"success": False, "errors": erros}, 422
            

            request.validated_data = validated_obj
            return f(*args, **kwargs)
        return wrapper
    return decorator
