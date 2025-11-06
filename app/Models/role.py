'''from app.Models.base_model import BaseDBModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Table, Column, Integer, ForeignKey
from app.extensions import db
from app.Models.relations import user_roles, roles_permissions
from app.Models.base_model import BaseDBModel

user_roles = Table(
    "user_roles",
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('roles_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True)
) 


class Role(BaseDBModel):
    __tablename__ = "roles"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description : Mapped[str] = mapped_column(Text)
    
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=roles_permissions, back_populates="roles")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }'''