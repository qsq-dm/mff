"""empty message

Revision ID: 38dd6746c99b
Revises: 42d4367e28b2
Create Date: 2015-12-10 17:50:20.145840

"""

# revision identifiers, used by Alembic.
revision = '38dd6746c99b'
down_revision = '42d4367e28b2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coupon', sa.Column('is_trial', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('coupon', 'is_trial')
    ### end Alembic commands ###
