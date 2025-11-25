from flask_restful import Resource
from flask import request, current_app, g

from sqlalchemy.exc import SQLAlchemyError
from app.Decorators.rate_limit import rate_limit
from app.Models.datatype import Datatype
from app.Schemas.datatype import DatatypeSchema
from app.Mappers.datatype_mapper import DatatypeMapper

from app.Decorators.validation import validate_schema
from app.Decorators.filter_methods import auto_filter_method
from app.Util.response import suc_res, error_res
from app.Decorators.authentication import authenticate
from app.Decorators.authorization import access_required

from flasgger import swag_from
from app.Controllers.docs.datatypes import (DATATYPE_COLLECTION, DATATYPE_ITEM, DATATYPE_CREATE, DATATYPE_PUT)

class DatatypeResource(Resource):
    @property
    def service(self):
        return current_app.datatype_service
    
    @authenticate
    @access_required(resource="datatype", action="read")
    @auto_filter_method(Datatype)
    @swag_from(DATATYPE_COLLECTION)
    def get(self, filters=None):
        data = self.service.get(filters)
        if not data:
            return error_res([], 404)
        return suc_res(DatatypeMapper.to_list(data), 200)
                                 
    @authenticate              
    @access_required(resource="datatype", action="create")
    @rate_limit(10, 60)
    @validate_schema(DatatypeSchema)
    @swag_from(DATATYPE_CREATE)
    def post(self):
        data = request.get_json()
        data['creator_id'] = g.current_user_id
        try:
            dt = self.service.create(data)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(DatatypeMapper.to_dict(dt), 201)
    

class DatatypeIDResource(Resource):
    
    @property
    def service(self):
        return current_app.datatype_service
    
    @authenticate
    @access_required(resource="datatype", action="read")
    @swag_from(DATATYPE_ITEM)
    def get(self, id=None):
        if id is not None:
            dt = self.service.get_by_id(id)
            if not dt:
                return error_res([], 404)
            return suc_res(DatatypeMapper.to_dict(dt), 200)
    
    
    @authenticate
    @swag_from(DATATYPE_PUT)
    @access_required(resource="datatype", action="update")
    @validate_schema(DatatypeSchema)
    def put(self, id: int):
        data = request.get_json()
        try:
            dt = self.service.update(id, data)
        except ValueError as e:
            return error_res(str(e), 500)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(DatatypeMapper.to_dict(dt), 200)
    
    @authenticate
    @access_required(resource="datatype", action="delete")
    @swag_from(DATATYPE_ITEM)
    def delete(self, id: int):
        try:
            dt = self.service.delete(id)
            return suc_res({"msg": f"Deleted datatype '{dt.name}'"}, 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        

def register_routes(api):
    api.add_resource(DatatypeResource, '/datatype')
    api.add_resource(DatatypeIDResource, '/datatype/<int:id>')
