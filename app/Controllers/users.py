from flask_restful import Resource
from flask import current_app, request, g
from sqlalchemy.exc import SQLAlchemyError
from app.Schemas.user import UserCreateSchema
from app.Models.user import User

from app.Util.response import suc_res, error_res
from app.Decorators.filter_methods import auto_filter_method
from app.Decorators.validation import validate_schema
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required


class UserResource(Resource):
    
    @property
    def service(self):
        return current_app.user_service
    
    @authenticate
    @auto_filter_method(User)
    def get(self, id=None, filters=None):
        if id is not None:
            data = self.service.get_by_id(id)
            if not data:
                return error_res("User not found", 404)
            return suc_res(data, 200)
        
        data = self.service.get(filters)
        if not data:
            return error_res([], 404)
        return suc_res(data, 200)
    
    @authenticate
    @superadmin_required
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
            if not user:
                error_res("No role found ", 404)
        except ValueError as e:
            return error_res("No User or Role assigned ", 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(user, 201)
    
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
        return suc_res(role, 200)

    
def register_user_role_routes(api):
    api.add_resource(UserRoleResource, '/user/<int:user_id>/roles/<int:role_id>')