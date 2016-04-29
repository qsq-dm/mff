"""empty message

Revision ID: 282274e764ca
Revises: 2b4b8933851
Create Date: 2015-12-05 16:05:41.867941

"""

# revision identifiers, used by Alembic.
revision = '282274e764ca'
down_revision = '2b4b8933851'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promoter', sa.Column('follow_count', sa.Integer(), nullable=True))
    op.add_column('promoter', sa.Column('reg_count', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_promoter_follow_count'), 'promoter', ['follow_count'], unique=False)
    op.create_index(op.f('ix_promoter_reg_count'), 'promoter', ['reg_count'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_promoter_reg_count'), table_name='promoter')
    op.drop_index(op.f('ix_promoter_follow_count'), table_name='promoter')
    op.drop_column('promoter', 'reg_count')
    op.drop_column('promoter', 'follow_count')
    ### end Alembic commands ###