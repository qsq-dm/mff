"""empty message

Revision ID: 42e923c1238
Revises: None
Create Date: 2015-10-30 16:36:01.320765

"""

# revision identifiers, used by Alembic.
revision = '42e923c1238'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import models

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('passwd', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('coupon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('cat', mysql.TINYINT(display_width=1), nullable=False),
    sa.Column('effective', sa.Integer(), nullable=False),
    sa.Column('remark', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hospital',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=100), nullable=True),
    sa.Column('tags', sa.String(length=1000), nullable=True),
    sa.Column('addr', sa.String(length=300), nullable=True),
    sa.Column('long_lat', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_cat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('pay_notify_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pay_type', mysql.TINYINT(display_width=1), nullable=False),
    sa.Column('content', sa.String(length=10000), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('period_pay_choice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('period_count', sa.Integer(), nullable=False),
    sa.Column('period_fee', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('period_count')
    )
    op.create_table('school',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('city_name', sa.String(length=100), nullable=True),
    sa.Column('link', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('phone', sa.String(length=80), nullable=True),
    sa.Column('passwd', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('credit_apply',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('id_no', sa.String(length=18), nullable=True),
    sa.Column('school', sa.String(length=100), nullable=True),
    sa.Column('enrollment_time', sa.DateTime(), nullable=True),
    sa.Column('major', sa.String(length=100), nullable=True),
    sa.Column('stu_no', sa.String(length=20), nullable=True),
    sa.Column('stu_years', sa.Integer(), nullable=True),
    sa.Column('addr', sa.String(length=100), nullable=True),
    sa.Column('parent_contact', sa.String(length=100), nullable=True),
    sa.Column('chsi_name', sa.String(length=100), nullable=True),
    sa.Column('chsi_passwd', sa.String(length=100), nullable=True),
    sa.Column('id_card_photo', sa.String(length=100), nullable=True),
    sa.Column('stu_card_photo', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('credit_change_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_sub_cat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('desc', sa.String(length=1000), nullable=True),
    sa.Column('icon', sa.String(length=100), nullable=True),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['item_cat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_advice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=10000), nullable=True),
    sa.Column('contact', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_coupon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coupon_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cat', mysql.TINYINT(display_width=1), nullable=False),
    sa.Column('price', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('remark', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['coupon_id'], ['coupon.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_credit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('total', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('used', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wechat',
    sa.Column('open_id', sa.String(length=32), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('open_id')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('orig_price', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('price', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('sub_cat_id', sa.Integer(), nullable=False),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.Column('photos', sa.String(length=1000), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('item_no', sa.String(length=50), nullable=True),
    sa.Column('support_choices', sa.String(length=50), nullable=True),
    sa.Column('sold_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.ForeignKeyConstraint(['sub_cat_id'], ['item_sub_cat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('photos', sa.String(length=1000), nullable=True),
    sa.Column('content', sa.String(length=10000), nullable=True),
    sa.Column('rate', sa.Float(), nullable=True),
    sa.Column('is_anonymous', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_fav',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'item_id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pay_method', mysql.TINYINT(display_width=1), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('order_no', sa.String(length=30), nullable=True),
    sa.Column('credit_choice_id', sa.Integer(), nullable=True),
    sa.Column('coupon_id', sa.Integer(), nullable=True),
    sa.Column('coupon_amount', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('credit_amount', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('price', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('total', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.Column('credit_verified', mysql.TINYINT(display_width=1), nullable=False),
    sa.ForeignKeyConstraint(['coupon_id'], ['user_coupon.id'], ),
    sa.ForeignKeyConstraint(['credit_choice_id'], ['period_pay_choice.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('coupon_id'),
    sa.UniqueConstraint('order_no')
    )
    op.create_table('credit_use_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('cat', mysql.TINYINT(display_width=1), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.Column('remark', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('period_pay_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('fee', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('punish', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('period_pay_index', sa.Integer(), nullable=True),
    sa.Column('period_count', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('repayment_time', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=100), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    op.create_index(op.f('ix_service_code_code'), 'service_code', ['code'], unique=True)
    op.create_table('punish_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('log_id', sa.Integer(), nullable=True),
    sa.Column('amount', models.MoneyField(precision=10, scale=2), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['log_id'], ['period_pay_log.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('punish_log')
    op.drop_index(op.f('ix_service_code_code'), table_name='service_code')
    op.drop_table('service_code')
    op.drop_table('period_pay_log')
    op.drop_table('order_log')
    op.drop_table('credit_use_log')
    op.drop_table('order')
    op.drop_table('item_fav')
    op.drop_table('item_comment')
    op.drop_table('item')
    op.drop_table('wechat')
    op.drop_table('user_credit')
    op.drop_table('user_coupon')
    op.drop_table('user_advice')
    op.drop_table('item_sub_cat')
    op.drop_table('credit_change_log')
    op.drop_table('credit_apply')
    op.drop_table('user')
    op.drop_table('school')
    op.drop_table('period_pay_choice')
    op.drop_table('pay_notify_log')
    op.drop_table('item_cat')
    op.drop_table('hospital')
    op.drop_table('coupon')
    op.drop_table('city')
    op.drop_table('admin_user')
    ### end Alembic commands ###