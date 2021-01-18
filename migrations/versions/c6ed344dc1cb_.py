"""empty message

Revision ID: c6ed344dc1cb
Revises: a1e705260687
Create Date: 2021-01-18 11:47:16.518914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6ed344dc1cb'
down_revision = 'a1e705260687'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'description')
    op.drop_column('user', 'about')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('item', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###