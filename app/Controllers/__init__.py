
from flask import Blueprint
from flask_restful import Api
bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)


from app.Controllers import users, authenticate, datatype

users.register_routes(api)
authenticate.register_auth_routes(api)
authenticate.register_password_routes(api)
datatype.register_routes(api)
