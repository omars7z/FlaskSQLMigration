"""create Users model, alter datatypes table

Revision ID: 5120dd452d38
Revises: 754db478bde5
Create Date: 2025-11-01 07:41:29.776725+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

# revision identifiers, used by Alembic.
revision: str = '5120dd452d38'
down_revision: Union[str, Sequence[str], None] = '754db478bde5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
"""create Users model, alter datatypes table"""

def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    try:
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('name', sa.String(50), unique=True, nullable=False),
            sa.Column('email', sa.String(120), unique=True, nullable=False),
            sa.Column('password', sa.String(512), nullable=True),
            sa.Column('token', sa.String(256), nullable=True),
            sa.Column('flag', sa.Integer(), nullable=False, server_default="0"),
            sa.Column('time_created', sa.DateTime(), nullable=False, server_default=sa.text("now()"))
        )

        users_table = sa.table(
            'users',
            sa.column('name', sa.String),
            sa.column('email', sa.String),
            sa.column('password', sa.String),
            sa.column('token', sa.String),
            sa.column('flag', sa.Integer),
        )

        session.execute(
            sa.insert(users_table).values(
                name="system",
                email="system@gmail.com",
                password=generate_password_hash("default_pass"),
                # token=None,
                flag=3
            )
        )

        # add creator_id to datatypes
        op.add_column(
            'datatypes',
            sa.Column(
                'creator_id',
                sa.Integer(),
                nullable=True,
                server_default="1"
            )
        )
        op.create_foreign_key(
            "fk_datatypes_creator_id",
            "datatypes", "users",
            ["creator_id"], ["id"],
            ondelete="SET NULL"
        )

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    try:
        op.drop_constraint("fk_datatypes_creator_id", "datatypes", type_="foreignkey")
        op.drop_column("datatypes", "creator_id")

        op.drop_table("users")
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
