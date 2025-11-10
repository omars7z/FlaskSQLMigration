
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.extensions import db

user_roles = Table(
    "user_roles",
    db.Model.metadata,
    # Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

roles_permissions = Table(
    "roles_permissions",
    db.Model.metadata,
    # Column("id", Integer, primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)   