
from flask import Blueprint
from flask_restful import Api
bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)


from app.Controllers import users, authenticate, datatype, role, permissions, files

users.register_routes(api)
datatype.register_routes(api)

authenticate.register_auth_routes(api)
authenticate.register_password_routes(api)
authenticate.register_refresh_routes(api)

role.register_role_routes(api)
users.register_user_role_routes(api)

permissions.register_perm_routes(api)
role.register_role_perm_routes(api)

files.register_routes(api)