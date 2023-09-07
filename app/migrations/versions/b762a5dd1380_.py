"""empty message

Revision ID: b762a5dd1380
Revises: 0d9ae6a752d1, 978ae973a482
Create Date: 2023-09-07 15:02:46.324458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b762a5dd1380'
down_revision: Union[str, None] = ('0d9ae6a752d1', '978ae973a482')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
