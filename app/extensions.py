from flask_sqlalchemy import SQLAlchemy
import logging

#Lazy singleton
db = SQLAlchemy()
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
