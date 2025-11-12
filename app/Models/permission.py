from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from app.Models.base import BaseDBModel
from app.Models.relations import roles_permissions

class Permission(BaseDBModel):
    
    __tablename__ = "permissions"
    
    flags: Mapped[dict] = {
        "isActive": False,
    }
    
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    resource: Mapped[str] = mapped_column(String(50))
    action: Mapped[str] = mapped_column(String(50))
    flag: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str] = mapped_column(Text)
    
    roles = relationship("Role", secondary=roles_permissions, back_populates="permissions")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "resource": self.resource,
            "actions": self.action,
            "description": self.description,
        }
    