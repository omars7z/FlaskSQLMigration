'''from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, String, Text
from app.Models.relations import roles_permissions
from app.Models.base_model import BaseDBModel

roles_permissions = Table(
    "roles_permissions",
    db.Model.metadata,
    Column('roles_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True),
    Column('permissions_id', Integer, ForeignKey('permissions.id', ondelete="CASCADE"), primary_key=True)
) 

class Permission(BaseDBModel):
    
    __tablename__ = "permissions"
    
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    resource: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    
    roles = relationship("Role", secondary=roles_permissions, back_populates="permissions")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
    '''