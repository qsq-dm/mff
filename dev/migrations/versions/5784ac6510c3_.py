"""empty message

Revision ID: 5784ac6510c3
Revises: 345ee23bca8
Create Date: 2015-12-09 18:03:16.566805

"""

# revision identifiers, used by Alembic.
revision = '5784ac6510c3'
down_revision = '345ee23bca8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trial_apply', sa.Column('cat', sa.Integer(), nullable=True))
    op.add_column('trial_apply', sa.Column('coupon_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'trial_apply', 'coupon', ['coupon_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trial_apply', type_='foreignkey')
    op.drop_column('trial_apply', 'coupon_id')
    op.drop_column('trial_apply', 'cat')
    ### end Alembic commands ###