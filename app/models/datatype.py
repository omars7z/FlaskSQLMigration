from app.extensions import db
import sqlalchemy as sa
from datetime import datetime
from app.models.flags import Flag

class Datatype(Flag, db.Model):
    __tablename__ = "datatypes"

    schema = {
        "canDoMathOperation": False,  # 1
        "canDoLogicalOperation": True,  # 2
        "isIterable": False  # 4
    }
    
    id = db.Column(sa.Integer, primary_key=True)
    name = db.Column(sa.String(50), unique=True, nullable=False)
    time_created = db.Column(sa.DateTime, default=datetime.now)
    example = db.Column(sa.JSON)
    flag = db.Column(sa.Integer, default=0)

    def __init__(self, request_param: dict):
        # ini flag with the dict
        name, example, flags = request_param.values()
        super().__init__(flags=flags, schema=self.schema)
        self.name = name
        self.example = example
        self.time_created = datetime.now()


    def to_dict(self):
        cr_flag = Flag(self.flag, schema=self.schema).to_dict()
        return {
            "id": self.id,
            "name": self.name,
            "example": self.example,
            "time_created": self.time_created.isoformat() if self.time_created else None,
            "flag": self.flag,
            "flags_map": cr_flag,
        }
