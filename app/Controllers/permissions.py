from flask_restful import Resource
from flask import request, current_app
from sqlalchemy.exc import SQLAlchemyError
from flasgger import swag_from

from app.Models.permission import Permission
from app.Schemas.permission import PermissionSchema
from app.Mappers.perm_mapper import PermMapper

from app.Util.response import suc_res, error_res
from app.Decorators.validation import validate_schema
from app.Decorators.filter_methods import auto_filter_method
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required

from app.Controllers.docs.permissions import PERM_ALL, PERM_ID, PERM_CREATE


class PermissionResource(Resource):

    @property
    def service(self):
        return current_app.permission_service

    @authenticate
    @auto_filter_method(Permission)
    @swag_from(PERM_ALL)
    def get(self, filters=None):
        try:
            perms = self.service.get(filters) or []
            return suc_res(PermMapper.to_list(perms), 200)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

    @authenticate
    @superadmin_required
    @validate_schema(PermissionSchema)
    @swag_from(PERM_CREATE)
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return error_res("No data found", 404)
            perm = self.service.create_permission(**data)
            return suc_res(PermMapper.to_dict(perm), 201)
        except ValueError as e:
            return error_res(str(e), 400)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)


class PermissionIDResource(Resource):

    @property
    def service(self):
        return current_app.permission_service

    @authenticate
    @swag_from(PERM_ID)
    def get(self, perm_id: int):
        try:
            user = self.service.get_by_id(perm_id)
            if not user:
                return error_res(f"User with id={perm_id} not found", 404)
            return suc_res(PermMapper.to_dict(user), 200)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

    @authenticate
    @superadmin_required
    @validate_schema(PermissionSchema)
    @swag_from(PERM_ID)
    def put(self, perm_id: int):
        try:
            data = request.get_json()
            perm = self.service.update_permission(perm_id, data)
            return suc_res(PermMapper.to_dict(perm), 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

    @authenticate
    @superadmin_required
    @swag_from(PERM_ID)
    def delete(self, perm_id: int):
        try:
            self.service.delete_permission(perm_id)
            return suc_res(f"Deleted permission id: {perm_id}", 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

def register_perm_routes(api):
    api.add_resource(PermissionResource, '/permission')
    api.add_resource(PermissionIDResource, '/permission/<int:perm_id>')
