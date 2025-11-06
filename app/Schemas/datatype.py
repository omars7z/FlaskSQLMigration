from marshmallow import Schema, fields, validates, ValidationError, post_load


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
    
    @validates('name')
    def validate_name(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError("Name cannot be empty")
        
    @validates('example')
    def validate_example(self, value, **kwargs):
        """Validate example structure"""
        if value is None:
            return
        
        if not isinstance(value, dict):
            raise ValidationError("Example must be a dictionary")
        
        for key, val in value.items():
            if val is not None and not isinstance(val, (str, int, float, bool)):
                raise ValidationError(f"Invalid value type for key '{key}'. Must be string, number, boolean, or null")
    
    @post_load
    def process_data(self, data, **kwargs):
        """Process data after validation"""
        # Remove None values from example
        if 'example' in data and data['example']:
            data['example'] = {k: v for k, v in data['example'].items() if v is not None}
        
        return data
