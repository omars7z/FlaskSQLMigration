from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from app.util.response import suc_res, error_res
from app.util.cdecorator import validate_json

class DatatypeResource(Resource):
    def __init__(self):
        self.service = current_app.datatype_service

    def get(self, datatype_id = None):
        if datatype_id is None:
            dts = self.service.get_all()
            return suc_res([dt.to_dict() for dt in dts])
        else:
            dt = self.service.get_by_id(datatype_id)
            if not dt:
                return error_res("Datatype not found", 404)
            return suc_res(dt.to_dict())

        
    # @validate_json(Datatype.schema)
    def post(self):
        data = request.get_json()
        try:
            dt = self.service.create(data)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)

        return suc_res(dt.to_dict(), 201)
    
       
    def put(self, datatype_id):
        data = request.get_json()
        if not data:
            return error_res("Invalid JSON", 400)
        dt = self.service.update(datatype_id, data)
        if not dt:
            return error_res("Datatype not found", 404)
        return suc_res(dt.to_dict())


    def delete(self, datatype_id):
        dt = self.service.get_by_id(datatype_id)
        if not dt:
            return {"success": False, "msg": "Datatype not found"}
        try:
            self.service.delete(dt)
        except ValueError as e:
            return {"success": False, "msg": str(e)}
        return {"success": True, "msg": f"Deleted datatype '{dt.name}'"}
    
   