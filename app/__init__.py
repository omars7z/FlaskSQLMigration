from flask import Flask
from .extensions import db
from app.config import get_config
from app.Helpers.manager import load_repositries
from .Helpers.registry import init_services
from .Controllers import bp as api_bp
# from .Controllers.users_controller import bp as api_bp
from .Services import datatype_service
from .Services import user_service

def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object(get_config())

    db.init_app(app)
    
    '''Repositry -> Service -> Controller'''
    repositories = load_repositries()
    init_services(app, repositories)
    
    app.register_blueprint(api_bp)
    
    return app