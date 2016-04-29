"""empty message

Revision ID: 2aa3dc20f05b
Revises: 53a9d06e37ce
Create Date: 2015-10-31 14:18:51.577349

"""

# revision identifiers, used by Alembic.
revision = '2aa3dc20f05b'
down_revision = '53a9d06e37ce'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('item_no', sa.String(length=100), nullable=True))
    op.create_index(op.f('ix_item_item_no'), 'item', ['item_no'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_item_no'), table_name='item')
    op.drop_column('item', 'item_no')
    ### end Alembic commands ###
