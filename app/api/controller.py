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
        """GET datatypes by id, name, list, flags"""
        query_params = request.args.to_dict()
        case_sens = query_params.pop("case_sens", "true").lower() == "true"

        method_params = {
            "id": lambda v: self.service.get_by_id(int(v)),
            "name": lambda v: self.service.get_by_name(v, case_sens),
            **{flags: lambda v, f=flags: [dt for dt in self.service.get_all()
                                      if dt.flags_dict.get(f) == (v.lower()=="true")]
                    for flags in Datatype.flags_map.keys()                
               },
            "list": lambda v: self.service.get_all(),
        }

        for key, val in query_params.items():
            if key in method_params:
                result = method_params[key](val)
                if not result:
                    return error_res("No datatypes found", 404)
                if isinstance(result, list):
                    return suc_res([dt.to_dict() for dt in result])
                return suc_res(result.to_dict())
            else:
                return error_res(f"invalid json request: {query_params}", 400)
                                    

    
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
        if not data:
            return error_res("Datatype not found", 404)
        dt = self.service.get_by_id(self._id)
        if not dt:
            return error_res(f"Datatype with id={self._id} not found", 404)
        try:
            dt = self.service.update(self._id, data)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(dt.to_dict())

    @require_query_param("id", int)
    def delete(self):
        dt = self.service.get_by_id(self._id)
        if not dt:
            return error_res("Datatype not found", 404)
        try:
            self.service.delete(dt)
        except ValueError as e:
            return error_res(str(e), 403)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res({"msg": f"Deleted datatype '{dt.name}'"})


api.add_resource(DatatypeResource, '/datatype') 
                  