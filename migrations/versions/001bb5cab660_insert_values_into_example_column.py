"""insert values into example column

Revision ID: 001bb5cab660
Revises: cb3368c4e10d
Create Date: 2025-10-16 08:25:02.481554+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001bb5cab660'
down_revision: Union[str, Sequence[str], None] = 'cb3368c4e10d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    meta = sa.MetaData()
    meta.reflect(bind)
    
    data_types = sa.Table('data_types', meta, autoload_with=bind)
    
    default_examples = {
        'Int' : '42',
        'Dict' : "{'omar':'value'}",
        'Float' : '3.91',
    }
    
    
    for name, example in default_examples.items():
        op.execute(
            data_types.update()
            .where(data_types.c.example==name)
            .values(example=example)
        )
    
    op.execute(
        data_types.update()
        .where(data_types.c.example == None)
        .values(example="default ")
    )    
    


def downgrade() -> None:
    """Downgrade schema."""
    con = op.get_bind()
    meta = sa.MetaData()
    meta.reflect(con)
    
    data_types = sa.Table('data_types', metadata=meta, autoload_with=con)
    op.excecute(data_types.update().values(example=None))