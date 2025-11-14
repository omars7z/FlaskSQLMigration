from flask_restful import Resource
from app.Schemas.login import LoginSchema
from app.Schemas.password import SetPasswordSchema

from app.Util.response import suc_res, error_res
from app.Decorators.validation import validate_schema

from app.Decorators.authentication import authenticate

from app.Util.jwt_token import create_access_token, create_refresh_token, decode_refresh_token
from app.Models.user import User

from flask import current_app, request, g

class LoginResource(Resource):
    
    @property
    def service(self):
        return current_app.auth_service
    
    @validate_schema(LoginSchema)
    def post(self):
        validated_data = request.validated_data
        email = validated_data["email"]
        password = validated_data["password"]
        user = self.service.login(email, password)
        if not user:
            return error_res("Wrong credentials", 404)
        
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        
        return suc_res({"msg": "Login successfully", "access_token": access_token, "refresh_token": refresh_token, }, 200)    

def register_auth_routes(api):
    api.add_resource(LoginResource, '/login')


class RefreshResource(Resource):
    
    @property
    def service(self):
        return current_app.auth_service
    
    # @authenticate
    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return error_res("Missing or wrong auth header", 401)

        token = auth_header.split(" ")[1]
        user_id = decode_refresh_token(token)

        if not user_id:
            return error_res("Wrong or expired refresh token", 404)
        
        user = User.query.get(user_id)
        # current_user = g.current_user
        # user = User.query.get(current_user)
        # ✅ Now user is a real object with `.id`
        new_access_token = create_access_token(user)
        return suc_res({
            "msg": " refreshed tokenn",
            "access_token": new_access_token
        }, 200)
        
def register_refresh_routes(api):
    api.add_resource(RefreshResource, '/refresh')
    
    
        # generate both access and refresh token in /login
        # middleware will only check access token
        # refresh token will be executed if the access token were expired and the refresh token still valid -> /refresh


    
class SetPasswordResource(Resource):
    
    @property
    def service(self):
        return current_app.auth_service
    
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
