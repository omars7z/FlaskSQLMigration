
PERM_ALL = {
    "tags": ["Permissions"],
    "summary": "Get all permissions or create a new permission",
    "description": "Retrieve all permissions or create a new permission (superadmin only for POST)",
    "parameters": [
        {
            "name": "filters",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "?name=edit_post"
        }
    ],
    "responses": {
        "200": {
            "description": "Permissions retrieved successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": True},
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "name": {"type": "string", "example": "edit_post"},
                                "description": {"type": "string", "example": "Can edit posts"}
                            }
                        }
                    }
                }
            }
        },
        "500": {"description": "Database error"}
    },
    "security": [{"Bearer": []}]
}

PERM_ID = {
    "tags": ["Permissions"],
    "summary": "Get, update, or delete a permission by ID",
    "description": "Retrieve, update or delete a specific permission by Id",
    "parameters": [
        {
            "name": "perm_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the permission"
        }
    ],
    "responses": {
        "200": {"description": "Permission retrieved or updated successfully"},
        "404": {"description": "Permission not found"},
        "500": {"description": "Database error"}
    },
    "security": [{"Bearer": []}]
}

PERM_CREATE = {
    'tags': ['Permissions'],
    'summary': 'Create a new permission',
    'description': 'Only superadmins can create permissions',
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name':        {'type': 'string', 'example': ' '},
                    'resource':    {'type': 'string', 'example': ' '},
                    'action':      {'type': 'string', 'example': 'art'},
                    'description': {'type': 'string', 'example': 'fa '}
                },
                'required': ['name', 'resource', 'action']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Permission created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id':          {'type': 'integer', 'example': 1},
                            'name':        {'type': 'string', 'example': 'dtomar'},
                            'resource':    {'type': 'string', 'example': 'datatype'},
                            'action':      {'type': 'string', 'example': 'art'},
                            'description': {'type': 'string', 'example': 'fa '}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Database error'
        }
    },
    'security': [{'Bearer': []}]
}
