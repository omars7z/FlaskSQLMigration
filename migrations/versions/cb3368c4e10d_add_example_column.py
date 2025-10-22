"""Add example column

Revision ID: cb3368c4e10d
Revises: 6035329b2efc
Create Date: 2025-10-16 03:23:37.854502+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb3368c4e10d'
down_revision: Union[str, Sequence[str], None] = '6035329b2efc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    con = op.get_bind()
    ins = sa.inspect(con)
    columns = [col['name'] for col in ins.get_columns('data_types')]
    if 'example' not in columns:
        op.add_column('data_types', sa.Column('example', sa.String(100), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('data_types', 'example')
