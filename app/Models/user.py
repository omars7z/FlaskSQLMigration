from app.Models.base import BaseDBModel
from typing import Optional
from sqlalchemy import Integer, String, DateTime
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app.Models.role import user_roles

class User(BaseDBModel):
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
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        """ <algorithm>:<hash function>:<iterations>$<salt>$<derived_key>
         pbkdf2:sha256:260000$uGbprVjZ6EbgmFlD$41e5d5fda0f6b28ef0a3cbe56e"""
         
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "flag": self.flag,
            "flags_map": self.to_dict_flags(),
        }
