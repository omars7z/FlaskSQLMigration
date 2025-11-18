FILE_LIST = {
    'tags': ['Files'],
    'summary': 'Get all uploaded files',
    'description': 'Retrieve a list of all uploaded files. Supports filters.',
    'parameters': [
        {
            'name': 'filters',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': '?uploader_id=1'
        }
    ],
    'responses': {
        '200': {
            'description': 'Files retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string', 'example': 'f_123abc'},
                                'name': {'type': 'string', 'example': 'image.png'},
                                'size': {'type': 'integer', 'example': 234234},
                                'uploader_id': {'type': 'integer', 'example': 1},
                                'created_at': {'type': 'string', 'example': '2025-01-01'}
                            }
                        }
                    }
                }
            }
        }
    },
    'security': [{'Bearer': []}]
}



FILE_UPLOAD = {
    'tags': ['Files'],
    'summary': 'Upload a new file',
    'description': 'Uploads a file and stores metadata.',
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'File to upload'
        }
    ],
    'responses': {
        '201': {
            'description': 'File uploaded successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'string', 'example': 'f_123abc'},
                            'name': {'type': 'string', 'example': 'file.png'},
                            'url': {'type': 'string', 'example': '/uploads/f_123abc.png'}
                        }
                    }
                }
            }
        },
        '400': {'description': 'Invalid file upload'}
    },
    'security': [{'Bearer': []}]
}



FILE_ITEM = {
    'tags': ['Files'],
    'summary': 'Get or update file metadata',
    'description': 'Retrieve or update a single file by ID',
    'parameters': [
        {
            'name': 'file_id',
            'in': 'path',
            'required': True,
            'type': 'string',
            'description': 'Unique file identifier'
        }
    ],
    'responses': {
        '200': {'description': 'File retrieved or updated successfully'},
        '404': {'description': 'File not found'}
    },
    'security': [{'Bearer': []}]
}



FILE_DELETE = {
    'tags': ['Files'],
    'summary': 'Delete a file',
    'description': 'Deletes the file and its record',
    'parameters': [
        {
            'name': 'file_id',
            'in': 'path',
            'required': True,
            'type': 'string',
            'description': 'Unique file identifier'
        }
    ],
    'responses': {
        '200': {'description': 'File deleted successfully'},
        '404': {'description': 'File not found'},
        '500': {'description': 'Database error'}
    },
    'security': [{'Bearer': []}]
}



DOWNLOAD = {
    "tags": ["Files"],
    "summary": "Download file",
    "description": "Downloads a file by ID.",
    "parameters": [
        {
            "name": "file_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    ],
    "responses": {
        200: {
            "description": "File download",
            "content": {
                "application/octet-stream": {
                    "example": "Binary file data"
                }
            }
        },
        404: {"description": "File not found"},
        500: {"description": "Error downloading file"}
    }
}


TEXT = {
    'tags': ['PDF'],
    'summary': 'Convert text to PDF',
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'description': 'Text content to convert to PDF'
                    }
                },
                'required': ['text']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'PDF file',
            'content': {
                'application/pdf': {
                    'schema': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        400: {
            'description': 'Text not provided'
        }
    }
}
