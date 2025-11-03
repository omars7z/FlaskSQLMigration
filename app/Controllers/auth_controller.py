from flask_restful import Resource
from flask import current_app, request

from app.decorators.marshmellow import validate_schema
from app.decorators.authentication import authenticate
from app.Util.response import suc_res, error_res


class AuthResource(Resource):
    
    @property
    def service(self):
        return current_app.user_service
    
    @validate_schema
    def post(self):
        
        user = request.validated_data
        email = user["email"]
        password = user["password"]
        
        log = self.service.login(email, password)
        if not log:
            return error_res("Wrong credintials", 404)
        
    