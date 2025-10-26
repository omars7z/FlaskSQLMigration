from app.extensions import db
import sqlalchemy as sa
from datetime import datetime
from .bitflag import BitFlag

class Datatype(db.Model):
    __tablename__ = "datatypes"

    flags_map = {
        "canDoMathOperation": False,
        "canDoLogicalOperation": True,
        "isIterable": False
    }

    id = db.Column(sa.Integer, primary_key=True)
    name = db.Column(sa.String(50), unique=True, nullable=False)
    time_created = db.Column(sa.DateTime, default=datetime.now)
    example = db.Column(sa.JSON)
    flag = db.Column(sa.Integer, default=0)
    is_deleted = db.Column(sa.Boolean, default=False)

    @property
    def flag_obj(self):
        return BitFlag(self.flags_map, self.flag)

    @property
    def flags_dict(self):
        return self.flag_obj.to_dict_flags()

    @property
    def flag_val(self):
        return self.flag_obj.get_flag()
    
    def set_flags(self, flags: dict):
        if self.flag is None:
            self.flag = 0
        for i, key in enumerate(self.flags_map.keys()):
            if key in flags:
                if flags[key]:
                    self.flag |= (1 << i)
                else:
                    self.flag &= ~(1 << i)
                    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "example": self.example,
            "time_created": self.time_created.isoformat(),
            "flag": self.flag,
            "flags_map": self.flags_dict,
            "is_deleted": self.is_deleted
        }