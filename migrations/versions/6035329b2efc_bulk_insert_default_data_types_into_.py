"""bulk insert default data types into data type table

Revision ID: 6035329b2efc
Revises: f79c10ba5af1
Create Date: 2025-10-14 09:51:19.104208+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.models.datatype import Datatype


# revision identifiers, used by Alembic.
revision: str = '6035329b2efc'
down_revision: Union[str, Sequence[str], None] = 'f79c10ba5af1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    meta = sa.MetaData()
    meta.reflect(bind=bind)
    
    dataTypes = sa.Table('data_types', meta, autoload_with=bind)
    # op.bulk_insert(dataTypes, [{ 'id': 1, 'name': 'abood', 'info': 'aaaaa' }])
    # pass
    op.bulk_insert(dataTypes, [
    {'id': 1, 'name': 'abood', 'info': 'aaaaa'},
    {'id': 2, 'name': 'Int', 'info': 'modified int type'},
    {'id': 3, 'name': 'Float', 'info': 'floating point type'},
    {'id': 4, 'name': 'Dict', 'info': 'dictionary key:val'},
])





def downgrade() -> None:
    """Downgrade schema."""
    con = op.get_bind()
    meta = sa.MetaData()
    meta.reflect(con)
    
    data_types = sa.Table('data_types', metadata=meta, autoload_with=con)
    op.excecute(data_types.update().values(example=None))