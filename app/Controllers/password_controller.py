from flask_restful import Resource
from flask import current_app, request
from app.Util.response import suc_res, error_res
from app.Decorators.authentication import authenticate


class PasswordResource(Resource):
    
    @property
    def service(self):
        return current_app.password_service
    
    
    @authenticate
    def post(self):
        data = request.get_json()
        token = data.get("token")
        password = data.get("password")
        user = self.service.set_password(token, password)
        if not user:
            return error_res("Invalid credintials: wrong sesion token", 401)
        return suc_res("password set succesfuly", 200)
    
    #forgot password, reset password