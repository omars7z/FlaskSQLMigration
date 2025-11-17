USER_ID = {
    'tags': ['Users'],
    'summary': 'Get or delete a user by ID',
    'description': 'Retrieve or delete a specific user by their ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the user'
        }
    ],
    'responses': {
        '200': {'description': 'User retrieved or deleted successfully'},
        '404': {'description': 'User not found'}
    },
    'security': [{'Bearer': []}]
}

USER_COLLECTION = {
    'tags': ['Users'],
    'summary': 'Get all users or create a new user',
    'description': 'Retrieve all users or create a new user',
    'parameters': [
        {
            'name': 'filters',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter users, e.g., ?name=John'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successfully retrieved users',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'name': {'type': 'string', 'example': 'John Doe'},
                                'email': {'type': 'string', 'example': 'john@example.com'}
                            }
                        }
                    }
                }
            }
        },
        '404': {'description': 'User not found'}
    },
    'security': [{'Bearer': []}]
}

USER_CREATE = {
    'tags': ['Users'],
    'summary': 'Create a new user',
    'description': 'Only superadmins can create users',
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'John Doe'},
                    'email': {'type': 'string', 'example': 'john@example.com'},
                },
                'required': ['name', 'email']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': 'John Doe'},
                            'email': {'type': 'string', 'example': 'john@example.com'}
                        }
                    }
                }
            }
        }
    },
    'security': [{'Bearer': []}]
}


USER_ROLE = {
    "tags": ["Users"],
    "summary": "Assign or remove a role to/from a user",
    "description": "Assign or remove a role",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the user"
        },
        {
            "name": "perm_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the role"
        }
    ],
    "responses": {
        "200": {"description": "role removed successfully"},
        "201": {"description": "role assigned successfully"},
        "404": {"description": "User or role not found"},
        "500": {"description": "Database error"}
    },
    "security": [{"Bearer": []}]
}
