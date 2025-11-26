import logging
import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship as sa_relationship

#Lazy singleton
db = SQLAlchemy()
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


def set_relationship(*args, **kwargs):
    if "lazy" not in kwargs:
        kwargs["lazy"] = "noload"  #set loading tyep
    return sa_relationship(*args, **kwargs)

sqlalchemy.orm.relationship = set_relationship
#by default it will retrieve only the record of the model and i can manuly get their relatoinship