"""empty message

Revision ID: 4806ede530e3
Revises: 503198b95377
Create Date: 2015-11-23 11:34:07.511517

"""

# revision identifiers, used by Alembic.
revision = '4806ede530e3'
down_revision = '503198b95377'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item_comment', sa.Column('is_re_comment', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item_comment', 'is_re_comment')
    ### end Alembic commands ###