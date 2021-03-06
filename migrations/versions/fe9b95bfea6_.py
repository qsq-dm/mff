"""empty message

Revision ID: fe9b95bfea6
Revises: 4eefa5b6eb51
Create Date: 2015-11-28 15:09:32.579622

"""

# revision identifiers, used by Alembic.
revision = 'fe9b95bfea6'
down_revision = '4eefa5b6eb51'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('note', sa.String(length=500), nullable=True))
    op.add_column('item', sa.Column('use_time', sa.String(length=300), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'use_time')
    op.drop_column('item', 'note')
    ### end Alembic commands ###
