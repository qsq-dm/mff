"""empty message

Revision ID: 55f4c256c989
Revises: 10f3ed6c72ed
Create Date: 2015-11-27 16:58:52.410295

"""

# revision identifiers, used by Alembic.
revision = '55f4c256c989'
down_revision = '10f3ed6c72ed'

from alembic import op
import sqlalchemy as sa
import models


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('total_fee', models.MoneyField(precision=10, scale=2), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'total_fee')
    ### end Alembic commands ###
