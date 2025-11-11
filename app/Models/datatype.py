from app.Models.base import BaseDBModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, Dict, Any
from sqlalchemy import Integer, String, JSON, DateTime, ForeignKey
from datetime import datetime
from app.Models.user import User


class Datatype(BaseDBModel):
    __tablename__ = "datatypes"

    flags: Dict[str, bool] = {
        "cantBeDeleted": False,
        "canDoMathOperation": False,
        "canDoLogicalOperation": True,
        "isIterable": False,
        "isDeleted": False,
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    example: Mapped[Optional[list[dict]]] = mapped_column(JSON)
    time_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    flag: Mapped[int] = mapped_column(Integer, default=0)

    creator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, default=1
    )
    creator = relationship("User", back_populates="datatypes")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "example": self.example,
            "time_created": self.time_created.isoformat(),
            "flag": self.flag,
            "flags": self.to_dict_flags(),
            "creator_id": self.creator_id,
        }
