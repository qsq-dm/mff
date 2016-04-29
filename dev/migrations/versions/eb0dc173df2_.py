"""empty message

Revision ID: eb0dc173df2
Revises: 32ca0414826f
Create Date: 2016-01-28 19:45:24.100057

"""

# revision identifiers, used by Alembic.
revision = 'eb0dc173df2'
down_revision = '32ca0414826f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin_user', sa.Column('city_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'admin_user', 'city', ['city_id'], ['id'])
    op.add_column('user', sa.Column('city_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'city', ['city_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'city_id')
    op.drop_constraint(None, 'admin_user', type_='foreignkey')
    op.drop_column('admin_user', 'city_id')
    ### end Alembic commands ###