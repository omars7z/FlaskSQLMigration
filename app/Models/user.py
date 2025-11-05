from app.Models.base_model import BaseModel2
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import Integer, String, DateTime
from datetime import datetime

class User(BaseModel2):
    __tablename__ = "users"

    flags_map = {
        "isActive": False,
        "isSuperAdmin": False,
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password: Mapped[Optional[str]] = mapped_column(String(512))
    token: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    flag: Mapped[int] = mapped_column(Integer, default=0)
    time_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    datatypes= relationship("Datatype", back_populates="creator", foreign_keys="[Datatype.creator_id]")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "flag": self.flag,
            "flags_map": self.to_dict_flags(),
        }
