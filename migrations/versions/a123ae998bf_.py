"""empty message

Revision ID: a123ae998bf
Revises: 36d5b6be1479
Create Date: 2015-11-11 17:01:19.461450

"""

# revision identifiers, used by Alembic.
revision = 'a123ae998bf'
down_revision = '36d5b6be1479'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('image', sa.String(length=300), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'image')
    ### end Alembic commands ###
