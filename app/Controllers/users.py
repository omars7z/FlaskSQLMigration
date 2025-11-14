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

import os
from flasgger import swag_from
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GET_USER = os.path.join(CURRENT_DIR, 'docs', 'users', 'get_user.yml')
CREATE_USER = os.path.join(CURRENT_DIR, 'docs', 'users', 'create_user.yml')
DELETE_USER = os.path.join(CURRENT_DIR, 'docs', 'users', 'delete_user.yml')

class UserResource(Resource):
    
    @property
    def service(self):
        return current_app.user_service
    
    @authenticate
    @auto_filter_method(User)
    @swag_from(GET_USER)
    def get(self, id=None, filters=None):
        if id is not None:
            user = self.service.get_by_id(id)
            if not user:
                return error_res("User not found", 404)
            return suc_res(UserMapper.to_dict(user), 200)
        
        users = self.service.get(filters) or []
        return suc_res(UserMapper.to_list(users), 200)
    
    @authenticate
    @superadmin_required
    @swag_from(CREATE_USER)
    @validate_schema(UserCreateSchema)
    def post(self):
        validated_user = request.validated_data
        try:
            user = self.service.create_user(
                name = validated_user["name"],
                email = validated_user["email"],
                # current_user=g.current_user
                )
            return suc_res({"msg":"User created", "token":user.token}, 201)
        except PermissionError as e:
            return error_res(str(e), 403)
       
       
    @authenticate
    @superadmin_required   
    @swag_from(DELETE_USER)
    def delete(self, id: int):
        try:
            user = self.service.delete_user(id)  
            return suc_res(f"Deleted user {user.name}", 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)


def register_routes(api):
    api.add_resource(UserResource, '/user', '/user/<int:id>')
    
    
class UserRoleResource(Resource):
    
    @property
    def service(self):
        return current_app.user_service
    
    @authenticate
    @superadmin_required
    def post(self, user_id: int, role_id: int):
        try:
            user = self.service.assign_role(user_id, role_id)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(UserMapper.to_dict(user), 201)
    
    @authenticate
    @superadmin_required
    def delete(self, user_id: int, role_id: int):
        try:
            user = self.service.remove_role(user_id, role_id)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(UserMapper.to_dict(user), 200)

    
def register_user_role_routes(api):
    api.add_resource(UserRoleResource, '/user/<int:user_id>/roles/<int:role_id>')