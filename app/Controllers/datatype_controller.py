from flask_restful import Resource
from flask import request, current_app, g

from sqlalchemy.exc import SQLAlchemyError
from app.Models.datatype import Datatype

from app.Decorators.marshmellow import validate_schema
from app.Decorators.cpost_decorator import validate_post
from app.Decorators.filter_methods import auto_filter_method
from app.Util.response import suc_res, error_res
from app.Decorators.authentication import authenticate

class DatatypeResource(Resource):
    @property
    def service(self):
        return current_app.datatype_service
    
    @authenticate
    @auto_filter_method(Datatype)
    def get(self, id = None, filters = None):
        if id is not None:
            data = self.service.get_by_id(id)
            if not data:
                return  error_res([], 404)
            return suc_res(data.to_dict(), 200)
        
        data = self.service.get(filters)
        if not data:
            return error_res([], 404)
        elif isinstance(data, list):
            return suc_res([dt.to_dict() for dt in data], 200)
        else:
            return error_res(f"invalid json request: {data}", 400)
                                 
    @authenticate                   
    @validate_post()
    @validate_schema(Datatype)
    def post(self):
        data = request.get_json()
        creator = g.current_user
        data['creator_id'] = creator.id
        try:
            dt = self.service.create(data)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(dt.to_dict(), 201)
    
    @authenticate
    @validate_schema(Datatype, partial=True)
    def put(self, id:int):
        data = request.get_json()
        dt = self.service.get_by_id(id)
        if not dt:
            return error_res(f"Datatype with id={id} not found", 404)
        try:
            dt = self.service.update(id, data) #here
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(dt.to_dict(), 200)
    
    @authenticate
    def delete(self, id:int):
        dt = self.service.get_by_id(id)
        if not dt:
            return error_res("Datatype with id={id} not found", 404)
        if dt.creator_id != g.current_user.id:
            return error_res("You are not allowed to delete this datatype", 403)
        try:
            self.service.delete(dt)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res({"msg": f"Deleted datatype '{dt.name}"}, 200)


