
from marshmallow import Schema, fields, validates, ValidationError

class UserCreateSchema(Schema):
    
    name = fields.String(required=True, validate=lambda x: 2 <= len(x) <= 50)
    email = fields.Email(required=True)
    isActive = fields.Boolean(required=False)
    isSuperAdmin = fields.Boolean(required=False)
    
    class Meta:
        ordered = True
        unknown = 'EXCLUDE'
    
    @validates('name')
    def validate_name(self, value,  **kwargs):
        """Validate name"""
        if not value.strip():
            raise ValidationError("Name cannot be empty")
