from flask_restful import Resource
from flask import request, current_app, g

from sqlalchemy.exc import SQLAlchemyError
from app.Models.permission import Permission

from app.Decorators.validation import validate_schema
from app.Decorators.filter_methods import auto_filter_method
from app.Util.response import suc_res, error_res
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required

class PermissionsResource(Resource):
    
    @property
    def service(self):
        return current_app.permissions_service
    
    def get(self, id:int=None, name:str=None):
        return
    

def register_routes(api):
    api.add_resource(PermissionsResource, '/user/<int:id>/roles/<string:name>/permissions')