from app.extensions import db
import sqlalchemy as sa
from datetime import datetime
from app.models.flags import Flag

class Datatype(Flag, db.Model):
    __tablename__ = "datatypes"

    schema = {
        "canDoMathOperation": False,  # 1
        "canDoLogicalOperation": True,  # 2
        "isIterable": False,  # 4
    }

    id = db.Column(sa.Integer, primary_key=True)
    name = db.Column(sa.String(50), unique=True, nullable=False)
    time_created = db.Column(sa.DateTime, default=datetime.now)
    example = db.Column(sa.JSON)
    flag = db.Column(sa.Integer, default=0)

    def set_flags(self, flags_dict: dict):
        flag_util = Flag(flags_dict, schema=self.schema)
        self.flag = flag_util.get_flag()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "example": self.example,
            "time_created": self.time_created.isoformat() if self.time_created else None,
            "flag": self.flag,
            "flags_map": self.schema,
        }
