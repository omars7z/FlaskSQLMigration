from flask import Flask
from .extensions import db
from .api.datatype_controller import bp as api_bp
from .Services.registry import init_services
from app.config import get_config
from app.Util.manager import load_repositries
from .Services import datatype_service

# def create_app():
def create_app(config_name):
    
    app = Flask(__name__)
    
    app.config.from_object(get_config())

    db.init_app(app)
    
    '''Repositry -> Service -> Controller'''
    repositories = load_repositries()
    init_services(app, repositories)
    
    app.register_blueprint(api_bp)
    
    return app