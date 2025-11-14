from flask import Flask
from flasgger import Swagger

from app.Config.swagger import swagger_config, swagger_template
from .extensions import db
from app.Config.app_config import get_config
from app.Helpers.manager import load_repositries, load_services
from .Helpers.registry import init_services
from .Controllers import bp as api_bp

def create_app():
    
    app = Flask(__name__)
    swagger = Swagger(app, config=swagger_config, template=swagger_template)
    app.config.from_object(get_config())

    db.init_app(app)
    
    '''Repositry -> Service -> Controller'''
    repositories = load_repositries()
    load_services()
    init_services(app, repositories)
    
    app.register_blueprint(api_bp)
    
    return app