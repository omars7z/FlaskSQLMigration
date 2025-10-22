"""add flag column

Revision ID: 787889c0ddb8
Revises: 001bb5cab660
Create Date: 2025-10-16 11:54:07.491262+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '787889c0ddb8'
down_revision: Union[str, Sequence[str], None] = '001bb5cab660'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('data_types', sa.Column('flag', sa.Integer(), server_default='0', nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('data_types', 'flag')
