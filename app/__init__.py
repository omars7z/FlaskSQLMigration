from flask import Flask
from .extensions import db
from .api.controller import bp as api_bp
from .repositries.datatype_repositry import DatatypeRepositry
from .services.registry import init_services
from app.config import get_config
from .services import datatype_service

def create_app(config_name):
    
    app = Flask(__name__)
    
    app.config.from_object(get_config())

    db.init_app(app)
    
    # Create repository instance and Inject repository into service
    # datatype_repo = DatatypeRepositry() #dynamic 
    # app.datatype_service = DatatypeService(datatype_repo) #dynamic
    repositories = {"Datatype": DatatypeRepositry()}
    init_services(app, repositories)
    
    app.register_blueprint(api_bp)
    
    return app