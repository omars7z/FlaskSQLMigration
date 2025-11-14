"""files migration

Revision ID: 9b761bfdddcc
Revises: c5193df0f33c
Create Date: 2025-11-13 09:25:59.572251+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.extensions import db
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision: str = '9b761bfdddcc'
down_revision: Union[str, Sequence[str], None] = 'c5193df0f33c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)
    try:
        op.create_table(
            'files',
            sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
            sa.Column('filename', sa.String(255), nullable=False),
            sa.Column('mime_type', sa.String(255), nullable=False),
            sa.Column('file_size', sa.BigInteger(), nullable=False),
            sa.Column('file_path', sa.String(500), nullable=False),
            sa.Column('time_created', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('uploader_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
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
        op.drop_table("files")
    except:
        session.rollback()
        raise
    finally:
        session.close()