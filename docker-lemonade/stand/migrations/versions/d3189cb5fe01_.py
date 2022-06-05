"""empty message

Revision ID: d3189cb5fe01
Revises: 2f2eb852559d
Create Date: 2018-03-02 16:58:09.525796

"""
from alembic import op
import sqlalchemy as sa
from stand.migration_utils import is_sqlite


# revision identifiers, used by Alembic.
revision = 'd3189cb5fe01'
down_revision = '2f2eb852559d'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cluster', sa.Column('executor_cores', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('cluster', sa.Column('executor_memory', sa.String(length=15), nullable=False, server_default='1G'))
    op.add_column('cluster', sa.Column('executors', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('cluster', sa.Column('general_parameters', sa.String(length=1000), nullable=False, server_default=''))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    if is_sqlite():
        with op.batch_alter_table('cluster') as batch_op:
            batch_op.drop_column('general_parameters')
            batch_op.drop_column('executors')
            batch_op.drop_column('executor_memory')
            batch_op.drop_column('executor_cores')
    else:
        op.drop_column('cluster', 'general_parameters')
        op.drop_column('cluster', 'executors')
        op.drop_column('cluster', 'executor_memory')
        op.drop_column('cluster', 'executor_cores')
    ### end Alembic commands ###
