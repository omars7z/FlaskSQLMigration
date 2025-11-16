from flask_restful import Resource
from flask import current_app, request, g
from app.Schemas.login import LoginSchema
from app.Schemas.password import SetPasswordSchema

from app.Util.response import suc_res, error_res
from app.Decorators.validation import validate_schema
from app.Decorators.refresh_jwt import refresh_jwt
from app.Util.jwt_token import create_access_token, create_refresh_token

import os
from flasgger import swag_from
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGIN = os.path.join(CURRENT_DIR, 'docs', 'auth', 'login.yml')
SET_PASS = os.path.join(CURRENT_DIR, 'docs', 'auth', 'set_password.yml')
REFRESH = os.path.join(CURRENT_DIR, "docs", "auth", "refresh.yml")


class LoginResource(Resource):

    @property
    def service(self):
        return current_app.auth_service

    @swag_from(LOGIN)
    @validate_schema(LoginSchema)
    def post(self):
        try:
            data = request.validated_data
            user = self.service.login(data["email"], data["password"])
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)

            return suc_res({
                "msg": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200)

        except ValueError as e:
            return error_res(str(e), 400)
        except Exception as e:
            return error_res(f"Internal server error: {str(e)}", 500)


def register_auth_routes(api):
    api.add_resource(LoginResource, '/login')


class RefreshResource(Resource):
    
    @property
    def service(self):
        return current_app.auth_service
    
    @refresh_jwt
    @swag_from(REFRESH)
    def post(self):
        new_access_token = create_access_token(g.current_user)
        return suc_res({
            "msg": "Refreshed tokenn",
            "new_access_token": new_access_token
        }, 200)
        
def register_refresh_routes(api):
    api.add_resource(RefreshResource, '/refresh')

    
class SetPasswordResource(Resource):
    
    @property
    def service(self):
        return current_app.auth_service
    
    @swag_from(SET_PASS)
    @validate_schema(SetPasswordSchema)
    def post(self):
        data = request.validated_data 
        token = data.get("token")
        password = data.get("password")
        try:
            self.service.set_password(token, password)
            return suc_res("password set succesfuly", 200)
        except ValueError as e:    
            return error_res(str(e), 401)
    
def register_password_routes(api):
    api.add_resource(SetPasswordResource, '/set_password')
