"""empty message

Revision ID: 35c5bd051538
Revises: 456050d473e
Create Date: 2016-02-02 14:29:50.529374

"""

# revision identifiers, used by Alembic.
revision = '35c5bd051538'
down_revision = '456050d473e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity', sa.Column('city_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'activity', 'city', ['city_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'activity', type_='foreignkey')
    op.drop_column('activity', 'city_id')
    ### end Alembic commands ###
