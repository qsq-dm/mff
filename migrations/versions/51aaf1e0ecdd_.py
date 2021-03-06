"""empty message

Revision ID: 51aaf1e0ecdd
Revises: a123ae998bf
Create Date: 2015-11-16 10:22:20.483272

"""

# revision identifiers, used by Alembic.
revision = '51aaf1e0ecdd'
down_revision = 'a123ae998bf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hospital', sa.Column('desc', sa.String(length=10000), nullable=True))
    op.add_column('hospital', sa.Column('working_time', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hospital', 'working_time')
    op.drop_column('hospital', 'desc')
    ### end Alembic commands ###
