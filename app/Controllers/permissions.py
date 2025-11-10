from flask_restful import Resource
from flask import request, current_app, g

from sqlalchemy.exc import SQLAlchemyError
from app.Models.permission import Permission
from app.Schemas.permission import PermissionSchema

from app.Decorators.validation import validate_schema
from app.Decorators.filter_methods import auto_filter_method
from app.Util.response import suc_res, error_res
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required

class PermissionsResource(Resource):
    
    @property
    def service(self):
        return current_app.permission_service

    # @authenticate
    @auto_filter_method(Permission)
    def get(self, perm_id=None, filters=None):
        if perm_id is not None:
            perm = self.service.get_by_id(perm_id)
            if not perm:
                return error_res(f"Permission with perm_id={perm_id} not found", 404)
            return suc_res(perm.to_dict(), 200)

        perms = self.service.get(filters)
        if not perms:
            return error_res([], 404)
        elif isinstance(perms, list):
            return suc_res([p.to_dict() for p in perms], 200)
        else:
            return error_res(f"invalid json request: {perms}", 400)

    @authenticate
    @superadmin_required
    @validate_schema(PermissionSchema)
    def post(self):
        data = request.get_json()
        if not data:
            return error_res("No data found", 404)
        try:
            perm = self.service.create_permission(**data)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)
        return suc_res(perm.to_dict(), 201)

    @authenticate
    @superadmin_required
    @validate_schema(PermissionSchema)
    def put(self, perm_id: int):
        perm = self.service.get_by_id(perm_id)
        if not perm:
            return error_res(f"Permission with id={perm_id} not found", 404)
        
        data = request.get_json()
        try:
            updated_perm = self.service.update_permission(perm, data)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)
        return suc_res(updated_perm.to_dict(), 200)

    @authenticate
    @superadmin_required
    def delete(self, perm_id: int):
        perm = self.service.get_by_id(perm_id)
        if not perm:
            return error_res(f"Permission with id={perm_id} not found", 404)
        try:
            self.service.delete_permission(perm_id)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)
        return suc_res(f"Deleted permission id: {perm_id}", 200)


    
def register_perm_routes(api):
    api.add_resource(PermissionsResource, '/permission', '/permission/<int:perm_id>')
    
    
class RolePermsionsResource(Resource):
    
    @property
    def service(self):
        return current_app.permission_service
    
    @authenticate
    @superadmin_required
    def post(self, user_id: int, perm_id: int):
        try:
            perm = self.service.assign_permission(user_id, perm_id)
            if not perm:
                error_res("No perm found ", 404)
        except ValueError as e:
            return error_res("No User or perm assigned ", 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(perm.to_dict(), 201)
    
    @authenticate
    @superadmin_required
    def delete(self, user_id: int, perm_id: int):
        try:
            perm = self.service.remove_permission(user_id, perm_id)
            if not perm:
                return error_res("User or perm not found", 404)
        except ValueError as e:
            return error_res("No User or perm assigned ", 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(perm.to_dict(), 200)


def register_role_perm_routes(api):
    api.add_resource(RolePermsionsResource, '/role/<int:role_id>/permission', '/role/<int:role_id>/permission/<int:perm_id>') #IMPORTANT
    