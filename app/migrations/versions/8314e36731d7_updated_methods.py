"""Updated Methods

Revision ID: 8314e36731d7
Revises: e71f8435c275
Create Date: 2023-09-05 18:54:19.703208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8314e36731d7'
down_revision: Union[str, None] = 'e71f8435c275'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
