"""add arithmetic operations

Revision ID: 2306652354f6
Revises: 787889c0ddb8
Create Date: 2025-10-16 14:06:08.339687+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import column, table


# revision identifiers, used by Alembic.
revision: str = '2306652354f6'
down_revision: Union[str, Sequence[str], None] = '787889c0ddb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('data_types', sa.Column('plus', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('data_types', sa.Column('minus', sa.Integer(), nullable=True, server_default='0'))

    data_types = table(
        'data_types',
        column('plus', sa.Integer),
        column('minus', sa.Integer)
    )
    op.execute(
        data_types.update().values(plus=0, minus=0)
    )

    op.alter_column('data_types', 'plus', server_default=None)
    op.alter_column('data_types', 'minus', server_default=None)



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('data_types', 'plus')
    op.drop_column('data_types', 'minus')
