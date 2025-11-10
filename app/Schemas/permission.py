from marshmallow import Schema, fields, validate

class PermissionSchema(Schema):
    
    id = fields.Int(dump_only=True)
    name =fields.Str(
        required=True,
        validate=validate.Length(min=2, max=50),
        error_messages={
            "required": "Permission name is required.",
            "null": "Permission name cannot be null.",
        })
    resource = fields.Str(
        required=False,
        validate=validate.Length(max=50),
        allow_none=True
        )
    action = fields.Str(   
        required=False,
        validate=validate.Length(max=50),
        allow_none=True
        )   
    description = fields.Str(
        required=False,
        allow_none=None
        )