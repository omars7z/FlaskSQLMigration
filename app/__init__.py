from flask import Flask
from dotenv import load_dotenv
from .extensions import db, mg
from .api import bp as api_bp
from .repositries.datatype_repositry import DatatypeRepositry
from .services.datatype_service import DatatypeService

def create_app(config_name):
    
    load_dotenv() #load env variables from .env
    
    app = Flask(__name__)
    
    app.config.from_object("app.config.Config")

    db.init_app(app)
    mg.init_app(app, db)
    
    # Create repository instance and Inject repository into service
    datatype_repo = DatatypeRepositry()
    app.datatype_service = DatatypeService(datatype_repo)

    app.register_blueprint(api_bp)
    
    return app