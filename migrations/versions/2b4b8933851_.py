"""empty message

Revision ID: 2b4b8933851
Revises: 4be704e34845
Create Date: 2015-12-05 14:38:14.004093

"""

# revision identifiers, used by Alembic.
revision = '2b4b8933851'
down_revision = '4be704e34845'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('qrcode', sa.Column('image', sa.String(length=300), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('qrcode', 'image')
    ### end Alembic commands ###
