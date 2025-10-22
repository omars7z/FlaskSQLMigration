from flask_restful import Resource
from flask import current_app
from app.util.response import suc_res, error_res

class DatatypeName(Resource):
    def __init__(self):
        self.service = current_app.datatype_service

    def get(self, datatype_name):
        dt = self.service.get_by_name(datatype_name)
        if not dt:
            return error_res(f"Datatype '{datatype_name}' not found", 404)
        return suc_res(dt.to_dict())
    
    
