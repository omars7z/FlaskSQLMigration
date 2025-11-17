ROLE_ALL= {
    "tags": ["Roles"],
    "summary": "Get all roles or create a new role",
    "description": "Retrieve all roles or create a new role",
    "parameters": [
        {
            "name": "filters",
            "in": "query",
            "type": "string",
            "required": False,
        }
    ],
    "responses": {
        "200": {
            "description": "Roles retrieved successfully",
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
                                "name": {"type": "string", "example": "Admin"},
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

ROLE_CREATE = {
    "tags": ["Roles"],
    "summary": "Create a new role",
    "description": "Create a new role (superadmin only)",
    "consumes": ["application/json"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Manager"},
                    "description": {"type": "string", "example": "Manager access"}
                },
                "required": ["name"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Role created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": True},
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "example": 2},
                            "name": {"type": "string", "example": "Manager"},
                            "description": {"type": "string", "example": "Manager access"}
                        }
                    }
                }
            }
        },
        "400": {"description": "Validation error"},
        "500": {"description": "Database error"}
    },
    "security": [{"Bearer": []}]
}

ROLE_ID = {
    "tags": ["Roles"],
    "summary": "Get, update, or delete a role by ID",
    "description": "Retrieve, update or delete a specific role by its ID",
    "parameters": [
        {
            "name": "role_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the role"
        }
    ],
    "responses": {
        "200": {"description": "Role retrieved or updated successfully"},
        "404": {"description": "Role not found"},
        "500": {"description": "Database error"}
    },
    "security": [{"Bearer": []}]
}

ROLE_PERMISSION = {
    "tags": ["Roles"],
    "summary": "Assign or remove a permission to/from a role",
    "description": "Assign or remove a permission",
    "parameters": [
        {
            "name": "role_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the role"
        },
        {
            "name": "perm_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the permission"
        }
    ],
    "responses": {
        "200": {"description": "Permission removed successfully"},
        "201": {"description": "Permission assigned successfully"},
        "404": {"description": "Role or permission not found"},
        "500": {"description": "Database error"}
    },
    "security": [{"Bearer": []}]
}
