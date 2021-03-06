"""empty message

Revision ID: 4ba5a6eafa93
Revises: 2aa3dc20f05b
Create Date: 2015-11-02 10:15:48.834451

"""

# revision identifiers, used by Alembic.
revision = '4ba5a6eafa93'
down_revision = '2aa3dc20f05b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospital_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('passwd', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hospital_user')
    ### end Alembic commands ###
