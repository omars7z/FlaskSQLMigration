from flask_restful import Resource
from app.Schemas.login import LoginSchema
from app.Schemas.password import SetPasswordSchema

from app.Util.response import suc_res, error_res
from app.Decorators.validation import validate_schema

from flask import current_app, request

class LoginResource(Resource):
    
    @property
    def service(self):
        return current_app.auth_service
    
    @validate_schema(LoginSchema)
    def post(self):
        validated_data = request.validated_data
        email = validated_data["email"]
        password = validated_data["password"]
        token = self.service.login(email, password)
        if not token:
            return error_res("Wrong credentials", 404)
        return suc_res({"msg": "Login successfully", "token": token}, 200)

def register_auth_routes(api):
    api.add_resource(LoginResource, '/login')

    
class SetPasswordResource(Resource):
    
    @property
    def service(self):
        return current_app.password_service
    
    @validate_schema(SetPasswordSchema)
    def post(self):
        data = request.validated_data 
        token = data.get("token")
        password = data.get("password")
        user = self.service.set_password(token, password)
        if not user:
            return error_res("Invalid credintials: wrong token", 401)
        return suc_res("password set succesfuly", 200)
    
def register_password_routes(api):
    api.add_resource(SetPasswordResource, '/set_password')