"""empty message

Revision ID: 4bbb37c90d8c
Revises: 13a5889df13
Create Date: 2016-03-09 10:49:01.279517

"""

# revision identifiers, used by Alembic.
revision = '4bbb37c90d8c'
down_revision = '13a5889df13'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_advice', sa.Column('remark', sa.String(length=300), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_advice', 'remark')
    ### end Alembic commands ###
