"""empty message

Revision ID: 4db11f101899
Revises: 4d043b343761
Create Date: 2015-12-09 15:21:29.065236

"""

# revision identifiers, used by Alembic.
revision = '4db11f101899'
down_revision = '4d043b343761'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trial',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=True),
    sa.Column('image', sa.String(length=300), nullable=True),
    sa.Column('cat', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('sent', sa.Integer(), nullable=True),
    sa.Column('apply_count', sa.Integer(), nullable=True),
    sa.Column('rules', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trial_apply',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('trial_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('school', sa.String(length=100), nullable=True),
    sa.Column('addr', sa.String(length=100), nullable=True),
    sa.Column('content', sa.String(length=1000), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['trial_id'], ['trial.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trial_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('trial_id', sa.Integer(), nullable=False),
    sa.Column('photos', sa.String(length=1000), nullable=True),
    sa.Column('content', sa.String(length=10000), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['trial_id'], ['trial.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trial_comment')
    op.drop_table('trial_apply')
    op.drop_table('trial')
    ### end Alembic commands ###
