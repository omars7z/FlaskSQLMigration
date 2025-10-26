from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from app.models.datatype import Datatype
from app.util.type_validator import validate_types
from app.util.post_validator import validate_post
from app.util.param_validator import require_query_param
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
        """GET datatypes by id, name, or list."""
        id = request.args.get("id", type=int)
        name = request.args.get("name")
        case_sens = request.args.get("case_sens", "true").lower() == "true"

        if id:
            dt = self.service.get_by_id(id)
            if not dt:
                return error_res(f"Datatype with id={id} not found", 404)
            return suc_res(dt.to_dict())

        elif name:
            dts = self.service.get_by_name(name, case_sens)
            if not dts:
                return error_res(f"Datatype with name='{name}' not found", 404)
            return suc_res([dt.to_dict() for dt in dts])

        else:
            dts = self.service.get_all()
            if not dts:
                return error_res("No datatypes found", 404)
            return suc_res([dt.to_dict() for dt in dts])
    
    
    # @validate_types(Datatype.flags_map)
    @validate_post(Datatype.flags_map)
    def post(self):
        data = request.get_json()
        try:
            dt = self.service.create(data)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)

        return suc_res(dt.to_dict(), 201)
    
       
    @require_query_param("id", int)
    def put(self):
        data = request.get_json()
        dt = self.service.update(self._id, data)
        if not dt:
            return error_res("Datatype not found", 404)
        return suc_res(dt.to_dict())

    @require_query_param("id", int)
    def delete(self):
        dt = self.service.get_by_id(self._id)
        if not dt:
            return error_res("Datatype not found", 404)
        try:
            self.service.delete(dt)
        except ValueError as e:
            return error_res(str(e), 400)
        return suc_res({"msg": f"Deleted datatype '{dt.name}'"})


api.add_resource(DatatypeResource, '/datatype') 
                  
# api.add_resource(DatatypeResource, '/datatype', 
#                  '/datatype/<int:id>',
#                  '/datatype/<string:name>' 
#                 ) 