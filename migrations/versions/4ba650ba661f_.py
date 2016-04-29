"""empty message

Revision ID: 4ba650ba661f
Revises: 3bed4aa05b5a
Create Date: 2015-12-07 10:15:09.015480

"""

# revision identifiers, used by Alembic.
revision = '4ba650ba661f'
down_revision = '3bed4aa05b5a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('qr_code_user', sa.Column('sex', sa.Integer(), nullable=True))
    op.add_column('qr_code_user', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'qr_code_user', 'user', ['user_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'qr_code_user', type_='foreignkey')
    op.drop_column('qr_code_user', 'user_id')
    op.drop_column('qr_code_user', 'sex')
    ### end Alembic commands ###