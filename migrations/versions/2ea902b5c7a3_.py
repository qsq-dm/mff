"""empty message

Revision ID: 2ea902b5c7a3
Revises: 5a62ecc7316e
Create Date: 2016-01-14 11:11:21.248504

"""

# revision identifiers, used by Alembic.
revision = '2ea902b5c7a3'
down_revision = '5a62ecc7316e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('beauty_entry', sa.Column('icon', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('beauty_entry', 'icon')
    ### end Alembic commands ###
