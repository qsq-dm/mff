"""empty message

Revision ID: 4593874013ba
Revises: 282274e764ca
Create Date: 2015-12-05 16:48:09.332665

"""

# revision identifiers, used by Alembic.
revision = '4593874013ba'
down_revision = '282274e764ca'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promoter_qrcode', sa.Column('qrcode_id', sa.Integer(), nullable=True))
    op.drop_index('ix_promoter_qrcode_scene_id', table_name='promoter_qrcode')
    op.create_foreign_key(None, 'promoter_qrcode', 'qrcode', ['qrcode_id'], ['id'])
    op.drop_column('promoter_qrcode', 'scene_id')
    op.add_column('qr_code_user', sa.Column('qrcode_id', sa.Integer(), nullable=True))
    op.drop_index('ix_qr_code_user_scene_id', table_name='qr_code_user')
    op.create_foreign_key(None, 'qr_code_user', 'qrcode', ['qrcode_id'], ['id'])
    op.drop_column('qr_code_user', 'scene_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('qr_code_user', sa.Column('scene_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'qr_code_user', type_='foreignkey')
    op.create_index('ix_qr_code_user_scene_id', 'qr_code_user', ['scene_id'], unique=False)
    op.drop_column('qr_code_user', 'qrcode_id')
    op.add_column('promoter_qrcode', sa.Column('scene_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'promoter_qrcode', type_='foreignkey')
    op.create_index('ix_promoter_qrcode_scene_id', 'promoter_qrcode', ['scene_id'], unique=False)
    op.drop_column('promoter_qrcode', 'qrcode_id')
    ### end Alembic commands ###