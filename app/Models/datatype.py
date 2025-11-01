from app.extensions import db
import sqlalchemy as sa
from datetime import datetime
from ..Util.base_model import BaseModel2
from typing import Optional, Dict, Any
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, JSON, ForeignKey

class Datatype(BaseModel2): #overide model class 
    __tablename__ = "datatypes"

    flags_map : Dict[str, bool]= {
        "cantBeDeleted": False, #1
        "canDoMathOperation": False, #2
        "canDoLogicalOperation": True, #4
        "isIterable": False, #8
        "isDeleted":False, #16
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    example: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    time_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    flag: Mapped[int] = mapped_column(Integer, default=0)
    
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), default=1)
    creator = relationship("User", back_populates="datatypes")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "example": self.example,
            "time_created": self.time_created.isoformat(),
            "flag": self.flag,
            "flags_map": self.to_dict_flags(),
        }