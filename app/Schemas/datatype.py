from marshmallow import Schema, fields, validates, ValidationError, post_load
import re
from app.Models.datatype import Datatype

class DatatypeSchema(Schema):
    
    name = fields.String(required=True, validate=lambda x: len(x) <= 50)
    example = fields.Dict(required=False, allow_none=True)
    creator_id = fields.Integer(required=False, allow_none=True)
    
    cantBeDeleted = fields.Boolean(required=False)
    canDoMathOperation = fields.Boolean(required=False)
    canDoLogicalOperation = fields.Boolean(required=False)
    isIterable = fields.Boolean(required=False)
    isDeleted = fields.Boolean(required=False)
    
    class Meta:
        ordered = True
        unknown = 'EXCLUDE'

    # --- NAME VALIDATION ---
    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError("Name cannot be empty")


    # --- EXAMPLE VALIDATION ---
    @validates("example")
    def validate_example(self, value, **kwargs):
        """Validate example structure and flag consistency"""
        if value is None:
            return
        
        if not isinstance(value, dict):
            raise ValidationError("Example must be a dictionary")
        
        for key, val in value.items():
            if val is not None and not isinstance(val, (str, int, float, bool)):
                raise ValidationError(
                    f"Invalid value type for key '{key}'. Must be string, number, boolean, or null"
                )

    # --- FLAG + EXAMPLE VALIDATION ---
    @post_load
    def process_data(self, data, **kwargs):

        flag_checks = {
            "canDoMathOperation": r"[\+\-\*/\^%]",
            "canDoLogicalOperation": r"\b(and|or|not|&|\|)\b",
            "isIterable": r"\b(for|while|loop|iter|range)\b"
        }

        errors = []
        example = data.get("example") or {}
        txts = [str(v).lower() for v in example.values()] if isinstance(example, dict) else []

        # validate flags and example 
        for flag, pattern in flag_checks.items():
            flag_val = data.get(flag, False)
            matching_pattern = any(re.search(pattern, txt) for txt in txts)

            if flag_val and not matching_pattern:
                errors.append(f"{flag} is True but example doesn't contain related content")
            if matching_pattern and not flag_val:
                errors.append(f"{flag} is False but example contains related content")

        if errors:
            raise ValidationError({"details": errors})

        return data
