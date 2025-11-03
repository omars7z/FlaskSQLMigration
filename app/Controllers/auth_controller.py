from flask_restful import Resource
from flask import current_app, request

from app.decorators.authentication import authenticate
from app.Util.response import suc_res, error_res


class AuthResource(Resource):
    
    @property
    def service(self):
        return current_app.user_service
    
    # @authenticate
    def post(self):
        
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        user = self.service.login(email, password)
        if not user:
            return error_res("Wrong cregfddintials", 404)
        return suc_res("login successfully", 200)
        
    