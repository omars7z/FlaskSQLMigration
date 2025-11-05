from flask import Flask
from .extensions import db
from app.config import get_config
from app.Helpers.manager import load_repositries, load_services
from .Helpers.registry import init_services
from .Controllers import bp as api_bp
def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object(get_config())

    db.init_app(app)
    
    '''Repositry -> Service -> Controller'''
    repositories = load_repositries()
    load_services()
    init_services(app, repositories)
    
    app.register_blueprint(api_bp)
    
    return app