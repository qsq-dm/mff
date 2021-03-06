"""empty message

Revision ID: 498586bf16c2
Revises: 3d1f1303d3e0
Create Date: 2016-03-03 10:54:43.656812

"""

# revision identifiers, used by Alembic.
revision = '498586bf16c2'
down_revision = '3d1f1303d3e0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('qr_code_user', sa.Column('status', mysql.TINYINT(display_width=1), nullable=True))
    op.create_index(op.f('ix_qr_code_user_status'), 'qr_code_user', ['status'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_qr_code_user_status'), table_name='qr_code_user')
    op.drop_column('qr_code_user', 'status')
    ### end Alembic commands ###
