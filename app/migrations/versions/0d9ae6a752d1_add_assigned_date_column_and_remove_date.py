"""Add assigned_date column and remove date

Revision ID: 0d9ae6a752d1
Revises: d77c56a21210
Create Date: 2023-09-07 09:23:23.552432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d9ae6a752d1'
down_revision: Union[str, None] = 'd77c56a21210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("inspections") as batch_op:
        batch_op.drop_column('date')
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('inspections', 'date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inspections', sa.Column('date', sa.DATE(), nullable=True))
    # ### end Alembic commands ###
