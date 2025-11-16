from marshmallow import Schema, fields, validates, ValidationError
import re

class LoginSchema(Schema):
    
    email = fields.String(required=True)
    password = fields.String(required=True)
    
    class Meta:
        ordered = True
        unknown = 'EXCLUDE'