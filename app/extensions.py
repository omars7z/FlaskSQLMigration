from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

#Lazy singleton
db = SQLAlchemy()
mg = Migrate()