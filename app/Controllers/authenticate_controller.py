from flask_restful import Resource
from flask import current_app, request

from app.Util.response import suc_res, error_res

class AuthenticateResource(Resource):
    
    @property
    def service(self):
        return current_app.user_service
    
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        token = self.service.login(email, password)
        if not token:
            return error_res("Wrong cregfddintials", 404)
        return suc_res({"yes":"login successfully", "token":token}, 200)
        
    