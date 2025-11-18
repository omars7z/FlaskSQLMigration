
DATATYPE_COLLECTION = {
    'tags': ['Datatypes'],
    'summary': 'Get all datatypes',
    'description': 'Retrieve all datatypes or filter them dynamically',
    'parameters': [
        {
            'name': 'filters',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter datatypes, e.g., ?name=Example'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successfully retrieved datatypes',
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
                                'name': {'type': 'string', 'example': 'Example'},
                                'creator_id': {'type': 'integer', 'example': 2}
                            }
                        }
                    }
                }
            }
        },
        '404': {'description': 'No datatypes found'}
    },
    'security': [{'Bearer': []}]
}

DATATYPE_ITEM = {
    'tags': ['Datatypes'],
    'summary': 'Get, update, or delete a datatype by ID',
    'description': 'Retrieve, update, or delete a specific datatype by its ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the datatype'
        }
    ],
    'responses': {
        '200': {'description': 'Datatype retrieved, updated, or deleted successfully'},
        '404': {'description': 'Datatype not found'},
        '400': {'description': 'Invalid JSON request'},
        '500': {'description': 'Database error'}
    },
    'security': [{'Bearer': []}]
}

DATATYPE_CREATE = {
    'tags': ['Datatypes'],
    'summary': 'Create a new datatype',
    'description': 'Only users with create permission can create a datatype',
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'NewDatatype'},
                    'description': {'type': 'string', 'example': 'Description of datatype'}
                },
                'required': ['name']
            }
        }
    ],
    'responses': {
        '201': {'description': 'Datatype created successfully'},
        '400': {'description': 'Invalid input'},
        '500': {'description': 'Database error'}
    },
    'security': [{'Bearer': []}]
}
