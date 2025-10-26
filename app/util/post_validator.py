from functools import wraps 
from flask import request 
from .response import error_res
import re
#if body has error return bad request 

def validate_post(flags_map: dict = None):
    
    flags_map = flags_map or None
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):#accept any combination of arguments (positional(1, 2, 3) + keyword {'a': 1, 'b': 2}
            
            data = request.get_json()
            if not data:
                return error_res("invalid JSON", 400)
        
            validated_data = {}
            for key in data:
                if key not in validated_data:
                    validated_data[key] = data[key]
            
            for key, default in flags_map.items():
                if key not in validated_data:
                    validated_data[key] = bool(default)


            example = validated_data.get("example")
            if not example:
                return error_res("Missing 'example' in request body", 400)
            
            examples = ""
            if isinstance(example, list):
                examples = example
            else:
                examples = [example]
                
            txt = " ".join(str(v).lower() for e in examples for v in e.values())
            
            errors = []
            
            if validated_data.get("canDoMathOperation"):
                if not re.search(r"[\+\-\*/\^%]", txt):
                    errors.append(" didn't find math expression like 2+1 4-4 ")
                    

            if validated_data.get("canDoLogicalOperation"):
                if not re.search(r"\b(and|or|not|&|\|)\b", txt):
                    errors.append(" should have logical operation like 'A and B'  '1 & 0'.")

                    
            if validated_data.get("isIterable"):
                if not re.search(r"\b(for|while|loop|iter|range)\b", txt):
                    errors.append(" should have iteration keyword like 'for' 'while' 'loop'.")
                    
            if errors:
                return error_res({"message":"wrong example content",
                          "details":errors},
                          400)
                 
            return f(*args, **kwargs)
        return wrapper
    return decorator 