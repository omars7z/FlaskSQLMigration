from flask_restful import Resource
from flask import current_app, request, g, make_response
from app.Decorators.rate_limit import rate_limit
from app.Schemas.login import LoginSchema
from app.Schemas.password import SetPasswordSchema

from app.Util.cookies import set_access_cookie
from app.Util.response import suc_res, error_res
from app.Decorators.validation import validate_schema
from app.Util.jwt_token import create_access_token

import os
from flasgger import swag_from
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGIN = os.path.join(CURRENT_DIR, 'docs', 'auth', 'login.yml')
SET_PASS = os.path.join(CURRENT_DIR, 'docs', 'auth', 'set_password.yml')


class LoginResource(Resource):

    @property
    def service(self):
        return current_app.auth_service

    @swag_from(LOGIN)
    @validate_schema(LoginSchema)
    @rate_limit(5, 60)
    def post(self):
        try:
            data = request.validated_data
            user = self.service.login(data["email"], data["password"])
            access_token = create_access_token(user)

            response_data = {
                "msg": "Login successful",
                "access_token": access_token,  
            }
            
            response = make_response(suc_res(response_data, 200))
            set_access_cookie(response, access_token)
            
            return response
        
        except ValueError as e:
            return error_res(str(e), 400)
        except Exception as e:
            print(e)
            return error_res(f"Internal server error: {str(e)}", 500)

    
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
    
    
def register_auth_routes(api):
    api.add_resource(LoginResource, '/login')
    api.add_resource(SetPasswordResource, '/set_password')
