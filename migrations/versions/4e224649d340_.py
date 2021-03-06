"""empty message

Revision ID: 4e224649d340
Revises: 4db11f101899
Create Date: 2015-12-09 15:44:31.540294

"""

# revision identifiers, used by Alembic.
revision = '4e224649d340'
down_revision = '4db11f101899'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coupon', sa.Column('item_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'coupon', 'item', ['item_id'], ['id'])
    op.add_column('trial', sa.Column('coupon_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'trial_ibfk_1', 'trial', type_='foreignkey')
    op.create_foreign_key(None, 'trial', 'coupon', ['coupon_id'], ['id'])
    op.drop_column('trial', 'item_id')
    op.add_column('user_coupon', sa.Column('item_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user_coupon', 'item', ['item_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_coupon', type_='foreignkey')
    op.drop_column('user_coupon', 'item_id')
    op.add_column('trial', sa.Column('item_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'trial', type_='foreignkey')
    op.create_foreign_key(u'trial_ibfk_1', 'trial', 'item', ['item_id'], ['id'])
    op.drop_column('trial', 'coupon_id')
    op.drop_constraint(None, 'coupon', type_='foreignkey')
    op.drop_column('coupon', 'item_id')
    ### end Alembic commands ###
