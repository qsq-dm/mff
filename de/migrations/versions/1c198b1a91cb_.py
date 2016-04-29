"""empty message

Revision ID: 1c198b1a91cb
Revises: 15e92c9ccee8
Create Date: 2015-12-14 14:13:25.240489

"""

# revision identifiers, used by Alembic.
revision = '1c198b1a91cb'
down_revision = '15e92c9ccee8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trial', sa.Column('start_time', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trial', 'start_time')
    ### end Alembic commands ###