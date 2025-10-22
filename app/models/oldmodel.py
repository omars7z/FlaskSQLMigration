'''from app.extensions import db
from datetime import datetime
from app.models.datatypeflags import DatatypeFlag

# sqlalchemy.orm.DeclarativeBas db.Modle singleton instance of SQLAlchemy
# db.Model is the Flask-SQLAlchemy base class (n

class Datatype(db.Model):
    __tablename__ = "data_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    info = db.Column(db.String(255))
    time_created = db.Column(db.DateTime, default=datetime.now)
    example = db.Column(db.String(255))
    flag = db.Column(db.Integer, default=0)

    @property
    def permissions_dict(self):
        return DatatypeFlag(self.flag).to_dict()
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info,
            "time": self.time_created.isoformat() if self.time_created else None,
            "example": self.example,
            "flag": self.flag,
            "permissions": self.permissions_dict  # use the property
        }
'''