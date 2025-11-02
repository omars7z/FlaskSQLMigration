from flask import Blueprint, current_app, request, g
from flask_restful import Resource, Api
from app.Models.user import User
from app.Util.response import suc_res, error_res
from app.decorators.filter_methods import auto_filter_method
from app.decorators.schema_validator import validate_schema

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)

class UserResource(Resource):
    
    @property
    def service(self):
        return current_app.user_service
    
    # @auth_required
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
    
    # @auth_required
    @validate_schema(User)
    def post(self):
        data = request.json_body()
        try:
            user = self.service.create_user(
                email=data["email"],
                password=data["password"],
                current_user = request.g.current_user
                )
            return suc_res({"msg":"User created", "token": user.token}, 201)
        except PermissionError as e:
            return error_res(str(e), 403)
    
    
api.add_resource(UserResource, '/user', '/user/<int:id>')