"""empty message

Revision ID: 29bbb2cfc971
Revises: 29347d4f2522
Create Date: 2016-01-28 11:21:45.024170

"""

# revision identifiers, used by Alembic.
revision = '29bbb2cfc971'
down_revision = '29347d4f2522'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('room_design_vote_log', sa.Column('source', mysql.TINYINT(display_width=1), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('room_design_vote_log', 'source')
    ### end Alembic commands ###
