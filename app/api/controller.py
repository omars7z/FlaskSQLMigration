from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from app.util.response import suc_res, error_res
from flask import Blueprint
from flask_restful import Api   

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)

class DatatypeResource(Resource):
    @property
    def service(self):
        return current_app.datatype_service
    
    def get(self):
        """GET datatypes by id, name, or all."""
        id = request.args.get("id", type=int)
        name = request.args.get("name")
        case_sens = request.args.get("case_sens", "true").lower() == "true"

        if id:
            dt = self.service.get_by_id(id)
            if not dt:
                return error_res(f"Datatype with id={id} not found", 404)
            return suc_res(dt.to_dict())

        elif name:
            dt = self.service.get_by_name(name, case_sens)
            if not dt:
                return error_res(f"Datatype with name='{name}' not found", 404)
            return suc_res(dt.to_dict())

        else:
            dts = self.service.get_all()
            if not dts:
                return error_res("No datatypes found", 404)
            return suc_res([dt.to_dict() for dt in dts])
    
    
    # @validate_json(Datatype)
    def post(self):
        data = request.get_json()
        try:
            dt = self.service.create(data)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)

        return suc_res(dt.to_dict(), 201)
    
       
    # @validate_json(Datatype.flags_map)
    def put(self):
        id = request.args.get("id", type=int)
        if not id:
            return error_res("Missing id", 400)
        data = request.get_json()
        dt = self.service.update(id, data)
        if not dt:
            return error_res("Datatype not found", 404)
        return suc_res(dt.to_dict())


    def delete(self):
        id = request.args.get("id", type=int)
        if not id:
            return error_res("Missing id, 404")
        dt = self.service.get_by_id(id)
        if not dt:
            return {"success": False, "msg": "Datatype not found"}
        try:
            self.service.delete(dt)
        except ValueError as e:
            return {"success": False, "msg": str(e)}
        return {"success": True, "msg": f"Deleted datatype '{dt.name}'"}


api.add_resource(DatatypeResource, '/datatype') 
                  
# api.add_resource(DatatypeResource, '/datatype', 
#                  '/datatype/<int:id>',
#                  '/datatype/<string:name>' 
#                 ) 