from flask import Blueprint
from flask_restful import Api
from app.api.controller import DatatypeResource
from app.api.namecontroller import DatatypeName

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)


api.add_resource(DatatypeResource, '/datatype', '/datatype/<int:datatype_id>')

api.add_resource(DatatypeName, '/name/<string:datatype_name>')
