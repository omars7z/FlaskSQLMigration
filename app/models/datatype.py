from app.extensions import db
import sqlalchemy as sa
from datetime import datetime

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

    def get_flag(self) -> int:
        return self.flag

    def to_int(self, flags: dict) -> int:
        val = 0
        for i, key in enumerate(self.flags_map.keys()):
            if flags.get(key, self.flags_map[key]):
                val |= (1 << i)
        return val

    def to_dict_flags(self) -> dict:
        return {key: bool(self.flag & (1 << i)) for i, key in enumerate(self.flags_map.keys())}

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
            "time_created": self.time_created.isoformat() if self.time_created else None,
            "flag": self.flag,
            "flags_map": self.to_dict_flags(),
            "is_deleted": self.is_deleted
        }

    def __repr__(self):
            return f"<DatatypeFlag {self.to_dict()} (int={self.flag})>"