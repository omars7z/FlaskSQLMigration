from marshmallow import Schema, fields, validates, ValidationError

class SetPasswordSchema(Schema):
    
    token = fields.String(required=True, validate=lambda x: len(x) > 10)
    password = fields.String(required=True, validate=lambda x: len(x) >= 5)
    
    class Meta:
        ordered = True
        unknown = 'EXCLUDE'
    
    @validates('password')
    def validate_password(self, value, **kwargs):
        if len(value) < 5:
            raise ValidationError("Password must be at least 5 characters")
        
        # at least one letter and  num
        has_letter = any(c.isalpha() for c in value)
        has_number = any(c.isdigit() for c in value)
        
        if not (has_letter and has_number):
            raise ValidationError("Password must contain at least one letter and one number")

