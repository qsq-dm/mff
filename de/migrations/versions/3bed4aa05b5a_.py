"""empty message

Revision ID: 3bed4aa05b5a
Revises: 4593874013ba
Create Date: 2015-12-05 17:49:05.566697

"""

# revision identifiers, used by Alembic.
revision = '3bed4aa05b5a'
down_revision = '4593874013ba'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wechat_location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('open_id', sa.String(length=50), nullable=True),
    sa.Column('lng', sa.String(length=50), nullable=True),
    sa.Column('lat', sa.String(length=50), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wechat_location_open_id'), 'wechat_location', ['open_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_wechat_location_open_id'), table_name='wechat_location')
    op.drop_table('wechat_location')
    ### end Alembic commands ###