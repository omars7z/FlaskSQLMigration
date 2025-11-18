import logging
from flask_sqlalchemy import SQLAlchemy

#Lazy singleton
db = SQLAlchemy()
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
