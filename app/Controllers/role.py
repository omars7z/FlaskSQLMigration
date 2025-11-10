from flask_restful import Resource
from flask import request, current_app, g

from sqlalchemy.exc import SQLAlchemyError
from app.Models.role import Role
from app.Schemas.role import RoleSchema

from app.Decorators.validation import validate_schema
from app.Decorators.filter_methods import auto_filter_method
from app.Util.response import suc_res, error_res
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required

class RoleResource(Resource):
    
    @property
    def service(self):
        return current_app.role_service
    
    @authenticate
    @auto_filter_method(Role)
    def get(self, role_id:int=None, filters=None):
        if role_id is not None:
            data = self.service.get_by_id(role_id)
            if not data:
                return error_res(f"User with id={role_id} not found", 404)
            return suc_res(data.to_dict(), 200)

        data = self.service.get(filters)
        if not data:
            return error_res([], 404)
        elif isinstance(data, list):
            return suc_res([dt.to_dict() for dt in data], 200)
        else:
            return error_res(f"invalid json request: {data}", 400)
    
    
    @authenticate
    @validate_schema(RoleSchema)
    def post(self):
        data = request.get_json()
        if not data:
            error_res("No data found ", 404)
        try:                
            dt = self.service.create_role(**data)
        except PermissionError as e:
            return error_res(str(e), 403)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(dt.to_dict(), 201)
    
    @authenticate
    @validate_schema(RoleSchema)
    def put(self, role_id:int):
        data = request.get_json()
        dt = self.service.get_by_id(role_id)
        if not dt:
            return error_res(f"Role with role_id={role_id} not found", 404)
        try:
            dt = self.service.update_role(role_id, data) 
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(dt.to_dict(), 200)
    
    @authenticate
    @superadmin_required
    def delete(self, role_id : int):
        data = self.service.get_by_id(role_id)
        if not data:
            error_res("No id found ", 404)
        try:                
            self.service.delete_role(role_id)
        except PermissionError as e:
            return error_res(str(e), 403)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(f"Deleted role id: {role_id}", 200)
        
         
def register_role_routes(api):
    api.add_resource(RoleResource, '/role', '/role/<int:role_id>')


class UserRoleResource(Resource):
    
    @property
    def service(self):
        return current_app.role_service
    
    @authenticate
    @superadmin_required
    def post(self, user_id: int, role_id: int):
        try:
            role = self.service.assign_role(user_id, role_id)
            if not role:
                error_res("No role found ", 404)
        except ValueError as e:
            return error_res("No User or Role assigned ", 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(role.to_dict(), 201)
    
    @authenticate
    @superadmin_required
    def delete(self, user_id: int, role_id: int):
        try:
            role = self.service.remove_role(user_id, role_id)
            if not role:
                return error_res("User or Role not found", 404)
        except ValueError as e:
            return error_res("No User or Role assigned ", 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(role.to_dict(), 200)

    
def register_user_role_routes(api):
    api.add_resource(UserRoleResource, '/user/<int:user_id>/roles/<int:role_id>')