import logging
import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship as sa_relationship

#Lazy singleton
db = SQLAlchemy()
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


def eager_relationship(*args, **kwargs):
    if "lazy" not in kwargs:
        kwargs["lazy"] = "joined"  #eager load
    return sa_relationship(*args, **kwargs)

sqlalchemy.orm.relationship = eager_relationship
