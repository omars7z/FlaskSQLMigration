"""add deleted dts column

Revision ID: ff851843918e
Revises: 754db478bde5
Create Date: 2025-10-25 05:37:14.448749+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff851843918e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('datatypes', sa.Column('is_deleted', sa.Boolean(), nullable=True, server_default='false'))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('datatypes', 'is_deleted')
