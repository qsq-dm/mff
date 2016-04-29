"""empty message

Revision ID: 18e507e87862
Revises: 3c12ca43b1ba
Create Date: 2015-12-31 09:52:12.246206

"""

# revision identifiers, used by Alembic.
revision = '18e507e87862'
down_revision = '3c12ca43b1ba'

from alembic import op
import sqlalchemy as sa
import models

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('beauty_entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('image', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recommend_beauty_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('daily_coupon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coupon_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('sent', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['coupon_id'], ['coupon.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'coupon', sa.Column('need', models.MoneyField(precision=10, scale=2), nullable=False))
    op.add_column(u'user_coupon', sa.Column('need', models.MoneyField(precision=10, scale=2), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'user_coupon', 'need')
    op.drop_column(u'coupon', 'need')
    op.drop_table('daily_coupon')
    op.drop_table('recommend_beauty_item')
    op.drop_table('beauty_entry')
    ### end Alembic commands ###
