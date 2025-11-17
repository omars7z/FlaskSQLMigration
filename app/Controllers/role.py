from flask_restful import Resource
from flask import request, current_app
from flasgger import swag_from

from app.Models.role import Role
from app.Schemas.role import RoleSchema
from app.Mappers.role_mapper import RoleMapper
from sqlalchemy.exc import SQLAlchemyError

from app.Util.response import suc_res, error_res
from app.Decorators.validation import validate_schema
from app.Decorators.filter_methods import auto_filter_method
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required

from app.Controllers.docs.roles import ROLE_ALL, ROLE_CREATE, ROLE_ID, ROLE_PERMISSION


class RoleResource(Resource):

    @property
    def service(self):
        return current_app.role_service

    @authenticate
    @auto_filter_method(Role)
    @swag_from(ROLE_ALL)
    def get(self, filters=None):
        try:
            roles = self.service.get(filters) or []
            return suc_res(RoleMapper.to_list(roles), 200)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

    @authenticate
    @validate_schema(RoleSchema)
    @swag_from(ROLE_CREATE)
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return error_res("No data found", 404)
            role = self.service.create_role(**data)
            return suc_res(RoleMapper.to_dict(role), 201)
        except ValueError as e:
            return error_res(str(e), 400)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)


class RoleIDResource(Resource):

    @property
    def service(self):
        return current_app.role_service

    @authenticate
    @swag_from(ROLE_ID)
    def get(self, role_id: int):
        try:
            user = self.service.get_by_id(role_id)
            if not user:
                return error_res(f"User with id={role_id} not found", 404)
            return suc_res(RoleMapper.to_dict(user), 200)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

    @authenticate
    @validate_schema(RoleSchema)
    @swag_from(ROLE_ID)
    def put(self, role_id: int):
        try:
            data = request.get_json()
            role = self.service.update_role(role_id, data)
            return suc_res(RoleMapper.to_dict(role), 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

    @authenticate
    @superadmin_required
    @swag_from(ROLE_ID)
    def delete(self, role_id: int):
        try:
            self.service.delete_role(role_id)
            return suc_res(f"Deleted role id: {role_id}", 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)


class RolePermissionResource(Resource):

    @property
    def service(self):
        return current_app.role_service

    @authenticate
    @superadmin_required
    @swag_from(ROLE_PERMISSION)
    def post(self, role_id: int, perm_id: int):
        try:
            role = self.service.assign_permission(role_id, perm_id)
            return suc_res(RoleMapper.to_dict(role), 201)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

    @authenticate
    @superadmin_required
    @swag_from(ROLE_PERMISSION)
    def delete(self, role_id: int, perm_id: int):
        try:
            self.service.remove_permission(role_id, perm_id)
            return suc_res(f"Removed perm id:{perm_id} from role id: {role_id}", 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)


def register_role_routes(api):
    api.add_resource(RoleResource, '/role')
    api.add_resource(RoleIDResource, '/role/<int:role_id>')
    api.add_resource(
        RolePermissionResource,
        '/role/<int:role_id>/permission/<int:perm_id>'
    )
