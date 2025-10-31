from functools import wraps
from flask import request, jsonify
from pydantic import BaseModel, ValidationError, create_model
from app.models.datatype import Datatype
from ..util.pydantic import sqlalchemy_to_pydantic
from ..util.response import suc_res, error_res

def validate_schema(sa_model):
    
    """
    Dynamic validator for post request JSON.
    """
    pydantic_model = sqlalchemy_to_pydantic(sa_model)
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            
            data = request.get_json() or {}
            try:
                validated_data = pydantic_model(**data)
            except ValidationError as e:
                return error_res({"success": False, "errors": e.errors()}), 422

            # Attach validated data to request
            request.validated_data = validated_data.model_dump()
            
            return f(*args, **kwargs)
        return wrapper
    return decorator