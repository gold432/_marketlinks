"""empty message

Revision ID: 49e41b320a71
Revises: 
Create Date: 2021-01-09 07:51:46.459970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49e41b320a71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('authorization_code', sa.Unicode(), nullable=True),
    sa.Column('bin', sa.Unicode(), nullable=True),
    sa.Column('last4', sa.Unicode(), nullable=True),
    sa.Column('exp_month', sa.Unicode(), nullable=True),
    sa.Column('exp_year', sa.Unicode(), nullable=True),
    sa.Column('card_type', sa.Unicode(), nullable=True),
    sa.Column('bank', sa.Unicode(), nullable=True),
    sa.Column('country_code', sa.Unicode(), nullable=True),
    sa.Column('brand', sa.Unicode(), nullable=True),
    sa.Column('account_name', sa.Unicode(), nullable=True),
    sa.Column('signature', sa.Unicode(), nullable=True),
    sa.Column('reusable', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=True),
    sa.Column('nation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['nation_id'], ['nation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('town',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=True),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['state_id'], ['state.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('place',
    sa.Column('name', sa.Unicode(), nullable=True),
    sa.Column('tags', sa.Unicode(), nullable=True),
    sa.Column('coordinates', sa.JSON(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('town_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['state_id'], ['state.id'], ),
    sa.ForeignKeyConstraint(['town_id'], ['town.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.JSON(), nullable=True),
    sa.Column('openby', sa.DateTime(), nullable=True),
    sa.Column('closedby', sa.DateTime(), nullable=True),
    sa.Column('online', sa.Boolean(), nullable=True),
    sa.Column('logo_url', sa.Unicode(), nullable=True),
    sa.Column('customer_code', sa.Unicode(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=True),
    sa.Column('email', sa.Unicode(length=123), nullable=True),
    sa.Column('name', sa.Unicode(length=123), nullable=True),
    sa.Column('password_hash', sa.String(length=123), nullable=True),
    sa.Column('description', sa.Unicode(length=123), nullable=True),
    sa.Column('about', sa.UnicodeText(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=373), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_table('cards',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('card_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['card_id'], ['card.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('archived', sa.Boolean(), nullable=True),
    sa.Column('itype', sa.Unicode(), nullable=True),
    sa.Column('location', sa.JSON(), nullable=True),
    sa.Column('viewed', sa.JSON(), nullable=True),
    sa.Column('price', sa.Unicode(), nullable=True),
    sa.Column('fields', sa.JSON(), nullable=True),
    sa.Column('json', sa.JSON(), nullable=True),
    sa.Column('name', sa.Unicode(), nullable=True),
    sa.Column('about', sa.Unicode(), nullable=True),
    sa.Column('paid_in', sa.Unicode(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('saved_places',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('saved_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('saved_items',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('item', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('saved_items')
    op.drop_table('saved_users')
    op.drop_table('saved_places')
    op.drop_table('item')
    op.drop_table('cards')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_table('user')
    op.drop_table('place')
    op.drop_table('town')
    op.drop_table('state')
    op.drop_table('nation')
    op.drop_table('card')
    # ### end Alembic commands ###
