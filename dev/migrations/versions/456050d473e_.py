"""empty message

Revision ID: 456050d473e
Revises: 34a7370fe40
Create Date: 2016-02-02 10:30:28.130061

"""

# revision identifiers, used by Alembic.
revision = '456050d473e'
down_revision = '34a7370fe40'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('redpack_question', sa.Column('status', mysql.TINYINT(display_width=1), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('redpack_question', 'status')
    ### end Alembic commands ###
