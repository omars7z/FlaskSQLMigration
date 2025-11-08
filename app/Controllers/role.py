from flask_restful import Resource
from flask import request, current_app, g

from sqlalchemy.exc import SQLAlchemyError
from app.Models.role import Role
# from app.Schemas.role import RoleSchema

from app.Decorators.validation import validate_schema
from app.Decorators.filter_methods import auto_filter_method
from app.Util.response import suc_res, error_res
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required

class RoleResource(Resource):
    
    @property
    def service(self):
    # def service():
        return current_app.user_service
    
    # @authenticate
    @auto_filter_method(Role)
    def get(self, id=None, filters=None):
        if id is not None:
            data = self.service.get_by_id(id)
            if not data:
                return error_res("User not found", 404)
            return suc_res(data.to_dict(), 200)

        data = self.service.get(filters)
        if not data:
            return error_res("User not found", 404)
        return suc_res([dt.to_dict() for dt in data], 200)
        
    # @authenticate
    @superadmin_required
    @validate_schema
    def post(self):
        pass
         
    
def register_routes(api):
    api.add_resource(RoleResource, '/user/<int:id>/roles', '/user/<int:id>/roles/<string:name>')