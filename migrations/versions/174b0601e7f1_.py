"""empty message

Revision ID: 174b0601e7f1
Revises: c2bb73ecf64
Create Date: 2016-01-05 11:10:04.014741

"""

# revision identifiers, used by Alembic.
revision = '174b0601e7f1'
down_revision = 'c2bb73ecf64'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    #xianpeng int > float stu_years
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('ALTER TABLE credit_apply modify stu_years float')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    #op.add_column('credit_apply', sa.Column('stu_years', mysql.FLOAT(), nullable=True))
    ### end Alembic commands ###
