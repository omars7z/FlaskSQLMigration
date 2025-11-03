from flask_restful import Resource
from flask import current_app, request
from app.Util.response import suc_res, error_res


class PasswordResource(Resource):
    
    @property
    def service(self):
        return current_app.user_service
    
    
    #@validate_schema always make custom? or how to make it ultra dynamic
    def post(self):
        data = request.get_json()
        token = data.get("token")
        password = data.get("password")
        user = self.service.set_password(token, password)
        if not user:
            error_res("Invalid credintials: wrong sesion token", 401)
        suc_res("password set succesfuly", 200)