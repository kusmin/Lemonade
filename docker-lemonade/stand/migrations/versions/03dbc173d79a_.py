"""Create table cluster_platform

Revision ID: 03dbc173d79a
Revises: 306f880b11c3
Create Date: 2019-07-02 09:51:57.061080

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql
from stand.migration_utils import (is_mysql, get_psql_enum_alter_commands,
        upgrade_actions, downgrade_actions, is_sqlite)

# revision identifiers, used by Alembic.
revision = '03dbc173d79a'
down_revision = '306f880b11c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cluster_platform',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('platform_id', sa.Integer(), nullable=False),
                    sa.Column('cluster_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['cluster_id'], ['cluster.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    if is_mysql():
        op.alter_column('job_step_log', 'message',
                    existing_type=mysql.LONGTEXT(),
                    nullable=False)
        op.execute("""
            ALTER TABLE cluster CHANGE `type` `type`
                ENUM('MESOS','YARN','SPARK_LOCAL','KUBERNETES')
                CHARSET utf8 COLLATE utf8_general_ci NOT NULL;
            """)
    elif is_sqlite():
        pass # No enum support in sqlite
    else:
        op.alter_column('job_step_log', 'message',
                    existing_type=sa.Text(),
                    nullable=False)
        values = ['MESOS','YARN','SPARK_LOCAL','KUBERNETES']
        all_commands = [[get_psql_enum_alter_commands(['cluster'], ['type'],
            'ClusterTypeEnumType', values, 'SPARK_LOCAL'), 
            None]]

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if is_mysql():
        op.alter_column('job_step_log', 'message',
                    existing_type=mysql.LONGTEXT(),
                    nullable=True)
    elif is_sqlite():
        pass # Keep cluster options
    else:
        pass # Keep cluster options
    op.drop_table('cluster_platform')
    # ### end Alembic commands ###
