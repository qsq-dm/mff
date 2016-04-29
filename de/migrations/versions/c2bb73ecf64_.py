"""empty message

Revision ID: c2bb73ecf64
Revises: 3c990682c3f0
Create Date: 2016-01-04 19:47:55.690716

"""

# revision identifiers, used by Alembic.
revision = 'c2bb73ecf64'
down_revision = '3c990682c3f0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alipay_order_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_no', sa.String(length=100), nullable=True),
    sa.Column('buyer_email', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_no')
    )
    op.create_index(op.f('ix_alipay_order_user_buyer_email'), 'alipay_order_user', ['buyer_email'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_alipay_order_user_buyer_email'), table_name='alipay_order_user')
    op.drop_table('alipay_order_user')
    ### end Alembic commands ###
