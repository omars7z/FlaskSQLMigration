from marshmallow import Schema, fields, validate

class RoleSchema(Schema):
    
    id = fields.Int(dump_only=True)
    name = fields.String(required=True,
                        validate=validate.Length(min=2, max=50),
                        error_messages={"required": "Role name is required"}
                        )
    description = fields.String(
        required=False,
        allow_none=True,
    )