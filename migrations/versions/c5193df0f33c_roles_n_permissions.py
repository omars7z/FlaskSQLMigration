"""Roles n Permissions

Revision ID: c5193df0f33c
Revises: 5120dd452d38
Create Date: 2025-11-05 13:52:05.925524+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision: str = 'c5193df0f33c'
down_revision: Union[str, Sequence[str], None] = '5120dd452d38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)
    try:
        op.create_table(
            'roles',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('name', sa.String(50), unique=True, nullable=False),
            sa.Column('description', sa.Text(), nullable=True, server_default="0"),
        )

        op.create_table(
            'permissions',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('name', sa.String(50), unique=True, nullable=False),
            sa.Column('resource', sa.String(50)),
            sa.Column('action', sa.String(50)),
            sa.Column('description', sa.Text(), nullable=True, server_default="0"),
        )
        
        op.create_table(
            'user_roles',
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="CASCADE")),
            sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id', ondelete="CASCADE"), nullable=False),
            sa.PrimaryKeyConstraint('user_id', 'role_id')
        )

        op.create_table(
            'roles_permissions',
            sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id', ondelete="CASCADE")),
            sa.Column('permission_id', sa.Integer(), sa.ForeignKey('permissions.id', ondelete="CASCADE")),
            sa.PrimaryKeyConstraint('role_id', 'permission_id')
        )

        
        roles_table = sa.table(
            'roles',
            sa.column('name', sa.String),
            sa.column('description', sa.Text),
        )
        
        session.execute(
            sa.insert(roles_table),
            [
                {
                    "name": "admin",
                    "description": "Administrator w all datatype permissions",
                },
                {
                    "name": "editor",
                    "description": "create, read, and update dtypes",
                },
                {
                    "name": "viewer",
                    "description": "Read only datatypes",
                }
            ]
        )
        
        permissions_table = sa.table(
            'permissions',
            sa.column('name', sa.String),
            sa.column('resource', sa.String),
            sa.column('action', sa.String),
            sa.column('description', sa.Text),
        )
        
        session.execute(
            sa.insert(permissions_table),
            [
                {
                    "name": "datatype:read",
                    "resource": "datatype",
                    "action": "read",
                    "description": "Perm to view datatypes",
                },
                {
                    "name": "datatype:delete",
                    "resource": "datatype",
                    "action": "delete",
                    "description": "Perm to delete any datatype",
                },
            ],
        )
        
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
    


def downgrade() -> None:
    """Downgrade schema."""
    
    bind = op.get_bind()
    session = Session(bind=bind)
    try:
        op.drop_table('roles_permissions')
        op.drop_table('user_roles')
        op.drop_table('permissions')
        op.drop_table('roles')
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()