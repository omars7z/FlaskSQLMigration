from flask_restful import Resource
from flask import request, current_app, g
from sqlalchemy.exc import SQLAlchemyError
from flasgger import swag_from

from app.Models.role import Role
from app.Schemas.role import RoleSchema
from app.Mappers.role_mapper import RoleMapper
from app.Decorators.validation import validate_schema
from app.Decorators.filter_methods import auto_filter_method
from app.Util.response import suc_res, error_res
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required

import os
from flasgger import swag_from
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROLES_SWAG = os.path.join(CURRENT_DIR, 'docs', 'roles', 'crud.yml')
ROLES_ACTION_SWAG = os.path.join(CURRENT_DIR, 'docs', 'roles', 'assigning.yml')

class RoleResource(Resource):
    
    @property
    def service(self):
        return current_app.role_service

    @authenticate
    @auto_filter_method(Role)
    @swag_from(ROLES_SWAG)
    def get(self, role_id: int = None, filters=None):
        if role_id is not None:
            role = self.service.get_by_id(role_id)
            if not role:
                return error_res(f"Role with id={role_id} not found", 404)
            return suc_res(RoleMapper.to_dict(role), 200)
        roles = self.service.get(filters) or []
        return suc_res(RoleMapper.to_list(roles), 200)

    @authenticate
    @validate_schema(RoleSchema)
    @swag_from(ROLES_SWAG)
    def post(self):
        data = request.get_json()
        if not data:
            return error_res("No data found", 404)
        try:                
            role = self.service.create_role(**data)
        except PermissionError as e:
            return error_res(str(e), 403)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(RoleMapper.to_dict(role), 201)

    @authenticate
    @validate_schema(RoleSchema)
    @swag_from(ROLES_SWAG)
    def put(self, role_id: int):
        data = request.get_json()
        try:
            role = self.service.update_role(role_id, data) 
        except ValueError as e:
            return error_res(str(e), 401)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(RoleMapper.to_dict(role), 200)

    @authenticate
    @superadmin_required
    @swag_from(ROLES_SWAG)
    def delete(self, role_id: int):
        try:                
            self.service.delete_role(role_id)
        except ValueError as e:
            return error_res(str(e), 403)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(f"Deleted role id: {role_id}", 200)


def register_role_routes(api):
    api.add_resource(RoleResource, '/role', '/role/<int:role_id>')


class RolePermsionsResource(Resource):
    
    @property
    def service(self):
        return current_app.role_service

    @authenticate
    @superadmin_required
    @swag_from(ROLES_ACTION_SWAG)
    def post(self, role_id: int, perm_id: int):
        try:
            role = self.service.assign_permission(role_id, perm_id)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(RoleMapper.to_dict(role), 201)

    @authenticate
    @superadmin_required
    @swag_from(ROLES_ACTION_SWAG)
    def delete(self, role_id: int, perm_id: int):
        try:
            self.service.remove_permission(role_id, perm_id)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(f"Removed perm id:{perm_id} from role id: {role_id}", 200)


def register_role_perm_routes(api):
    api.add_resource(
        RolePermsionsResource, '/role/<int:role_id>/permission/<int:perm_id>'
    )
