"""AddTables

Revision ID: b474e410dec4
Revises: 49002f4ac998
Create Date: 2024-11-10 19:08:36.326580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b474e410dec4'
down_revision: Union[str, None] = '49002f4ac998'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('content', sa.String(length=500), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.Column('parent_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('publisher_name', sa.String(), nullable=False),
    sa.Column('link_url', sa.String(), nullable=False),
    sa.Column('link_name', sa.String(), nullable=False),
    sa.Column('geo_tag', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('birthday', sa.DateTime(timezone=True), nullable=True),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.Column('education_info', sa.String(), nullable=False),
    sa.Column('registration_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('posts')
    op.drop_table('comments')
    # ### end Alembic commands ###