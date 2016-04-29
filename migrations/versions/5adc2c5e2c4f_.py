"""empty message

Revision ID: 5adc2c5e2c4f
Revises: 498586bf16c2
Create Date: 2016-03-03 13:59:11.264954

"""

# revision identifiers, used by Alembic.
revision = '5adc2c5e2c4f'
down_revision = '498586bf16c2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promoter', sa.Column('unfollow_count', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_promoter_unfollow_count'), 'promoter', ['unfollow_count'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_promoter_unfollow_count'), table_name='promoter')
    op.drop_column('promoter', 'unfollow_count')
    ### end Alembic commands ###
