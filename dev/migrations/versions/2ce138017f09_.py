"""empty message

Revision ID: 2ce138017f09
Revises: 38dd6746c99b
Create Date: 2015-12-10 19:14:00.636524

"""

# revision identifiers, used by Alembic.
revision = '2ce138017f09'
down_revision = '38dd6746c99b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_coupon', sa.Column('is_trial', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_coupon', 'is_trial')
    ### end Alembic commands ###
