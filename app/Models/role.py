from app.Models.base import BaseDBModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Table, Integer
from app.Models.relations import user_roles, roles_permissions

class Role(BaseDBModel):
    __tablename__ = "roles"
    
    flags: Mapped[dict] = {
        "isActive": False,
    }
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description : Mapped[str] = mapped_column(Text, nullable=True)
    flag: Mapped[int] = mapped_column(Integer, default=0)
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=roles_permissions, back_populates="roles")
    