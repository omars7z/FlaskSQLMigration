
from flask import Blueprint
from flask_restful import Api
bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)


from app.Controllers.users_controller import UserResource
from app.Controllers.password_controller import PasswordResource
from app.Controllers.authenticate_controller import AuthenticateResource
from app.Controllers.datatype_controller import DatatypeResource

api.add_resource(UserResource, '/user', '/user/<int:id>')
api.add_resource(PasswordResource, '/set_password')
api.add_resource(AuthenticateResource, '/login')
api.add_resource(DatatypeResource, '/datatype', '/datatype/<int:id>')