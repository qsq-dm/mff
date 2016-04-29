"""empty message

Revision ID: 1bef4d9bd99b
Revises: 58261a151f1d
Create Date: 2015-11-03 10:10:10.213077

"""

# revision identifiers, used by Alembic.
revision = '1bef4d9bd99b'
down_revision = '58261a151f1d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_code', sa.Column('book_time', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service_code', 'book_time')
    ### end Alembic commands ###
