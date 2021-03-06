"""Mail queue

Revision ID: 9f52309f0d44
Revises: e793fb176cbf
Create Date: 2020-03-25 10:49:23.112831

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from thorn.migration_utils import is_mysql

# revision identifiers, used by Alembic.
revision = '9f52309f0d44'
down_revision = '1fba1a39c681'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mail_queue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('attempts', sa.Integer(), nullable=False),
    sa.Column('json_data', mysql.LONGTEXT() if is_mysql() else sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mail_queue')
    # ### end Alembic commands ###
