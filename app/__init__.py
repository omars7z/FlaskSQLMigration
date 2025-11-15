from flask import Flask
from flasgger import Swagger

from .extensions import db
from .Controllers import bp as api_bp
from app.Config.swagger import swagger_config, swagger_template

from app.Config.settings import get_config
from app.Helpers.manager import load_repositries, load_services
from .Helpers.registry import init_services

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)
    
    '''Repo -> Service -> Controller'''
    repositories = load_repositries()
    load_services()
    init_services(app, repositories)
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    app.register_blueprint(api_bp)
    
    return app