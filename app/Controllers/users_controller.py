from flask_restful import Resource
from flask import current_app, request, g

from app.Models.user import User
from app.Util.response import suc_res, error_res
from app.decorators.filter_methods import auto_filter_method
from app.decorators.marshmellow import validate_schema
from app.decorators.authentication import authenticate



class UserResource(Resource):
    
    @property
    def service(self):
        return current_app.user_service
    
    # @authenticate
    @auto_filter_method(User)
    def get(self, id=None, filters=None, current_user=None):
        if id is not None:
            ''' Only (current_user) self can view user details
            if not current_user.id != id:
                return error_res("Access denied", 403)'''
            
            data = self.service.get_by_id(id)
            if not data:
                return error_res("User not found", 404)
            return suc_res(data.to_dict(), 200)
        
        
        data = self.service.get(filters)
        if not data:
            return suc_res([], 200)
        return suc_res([u.to_dict() for u in data], 200)
    
    # @authenticate
    @validate_schema(User)
    def post(self):
        # data = request.json_body()
        validated_user = request.validated_data
        try:
            user = self.service.create_user(
                name = validated_user.name,
                email = validated_user.name,
                current_user=getattr(g, "current_user", None)
                )
            return suc_res({"msg":"User created"}, 201)
        except PermissionError as e:
            return error_res(str(e), 403)
       
    