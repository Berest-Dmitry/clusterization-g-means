"""User_Updated_Foreign_UserId_Added

Revision ID: bd2dcc115ebf
Revises: 6865d7e2633e
Create Date: 2024-11-19 20:12:11.277125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd2dcc115ebf'
down_revision: Union[str, None] = '6865d7e2633e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('outer_service_id', sa.UUID(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'outer_service_id')
    # ### end Alembic commands ###