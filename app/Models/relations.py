
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.extensions import db
import sqlalchemy as sa

user_roles = Table(
    "user_roles",
    db.Model.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
    sa.UniqueConstraint("user_id", "role_id", name="uq_user_roles")
)

roles_permissions = Table(
    "roles_permissions",
    db.Model.metadata,
    Column("id", Integer, primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE")),
    sa.UniqueConstraint("role_id", "permission_id", name="uq_roles_permissions")    
)   