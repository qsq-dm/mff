"""empty message

Revision ID: 4deed7860ffe
Revises: 17354ab277c6
Create Date: 2015-12-19 11:40:41.995891

"""

# revision identifiers, used by Alembic.
revision = '4deed7860ffe'
down_revision = '17354ab277c6'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin_user', sa.Column('cat', mysql.TINYINT(display_width=1), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admin_user', 'cat')
    ### end Alembic commands ###
