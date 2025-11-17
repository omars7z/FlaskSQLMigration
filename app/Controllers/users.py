from flask_restful import Resource
from flask import current_app, request, g
from sqlalchemy.exc import SQLAlchemyError
from app.Schemas.user import UserCreateSchema
from app.Models.user import User
from app.Mappers.user_mapper import UserMapper

from app.Util.response import suc_res, error_res
from app.Decorators.filter_methods import auto_filter_method
from app.Decorators.validation import validate_schema
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required

from flasgger import swag_from
from app.Controllers.docs.users import USER_COLLECTION, USER_CREATE, USER_ID, USER_ROLE

class UserResource(Resource):

    @property
    def service(self):
        return current_app.user_service

    @authenticate
    @auto_filter_method(User)
    @swag_from(USER_COLLECTION)
    def get(self, filters=None):
        try:
            users = self.service.get(filters) or []
            return suc_res(UserMapper.to_list(users), 200)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)
        except Exception as e:
            return error_res(str(e), 500)

    @authenticate
    @superadmin_required
    @swag_from(USER_CREATE)
    @validate_schema(UserCreateSchema)
    def post(self):
        try:
            validated_user = request.validated_data
            user = self.service.create_user(
                name=validated_user["name"],
                email=validated_user["email"],
            )
            return suc_res({"msg": "User created", "token": user.token}, 201)
        except ValueError as e:
            return error_res(str(e), 400)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)


class UserIDesource(Resource):

    @property
    def service(self):
        return current_app.user_service

    @authenticate
    @swag_from(USER_ID)
    def get(self, id: int):
        try:
            user = self.service.get_by_id(id)
            if not user:
                return error_res(f"User with id={id} not found", 404)
            return suc_res(UserMapper.to_dict(user), 200)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

    @authenticate
    @superadmin_required
    @swag_from(USER_ID)
    def delete(self, id: int):
        try:
            user = self.service.delete_user(id)
            return suc_res(f"Deleted user {user.name}", 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)
        

class UserRoleResource(Resource):

    @property
    def service(self):
        return current_app.user_service

    @authenticate
    @superadmin_required
    @swag_from(USER_ROLE)
    def post(self, user_id: int, role_id: int):
        try:
            user = self.service.assign_role(user_id, role_id)
            return suc_res(UserMapper.to_dict(user), 201)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)

    @authenticate
    @superadmin_required
    @swag_from(USER_ROLE)
    def delete(self, user_id: int, role_id: int):
        try:
            user = self.service.remove_role(user_id, role_id)
            return suc_res(UserMapper.to_dict(user), 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res(f"Database error: {str(e)}", 500)


def register_user_routes(api):
    api.add_resource(UserResource, '/user',)
    api.add_resource(UserIDesource, '/user/<int:id>')
    api.add_resource(UserRoleResource, '/user/<int:user_id>/roles/<int:role_id>')