"""empty message

Revision ID: 5a62ecc7316e
Revises: 54d0e0d4445b
Create Date: 2016-01-11 16:35:18.455304

"""

# revision identifiers, used by Alembic.
revision = '5a62ecc7316e'
down_revision = '54d0e0d4445b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=True),
    sa.Column('desc', sa.String(length=1000), nullable=True),
    sa.Column('image', sa.String(length=300), nullable=True),
    sa.Column('link', sa.String(length=300), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification')
    op.drop_table('article')
    ### end Alembic commands ###