"""empty message

Revision ID: 82c208c2ff38
Revises: 35693eb8cdde
Create Date: 2020-08-10 18:54:03.784044

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from stand.migration_utils import is_psql, is_sqlite

# revision identifiers, used by Alembic.
revision = '82c208c2ff38'
down_revision = '35693eb8cdde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###a
    if is_psql():
        job_type_enum = postgresql.ENUM('APP', 'NORMAL', 'BATCH', name='JobTypeEnumType')
        job_type_enum.create(op.get_bind())

    op.add_column('job', sa.Column('type', sa.Enum('APP', 'NORMAL', 'BATCH', name='JobTypeEnumType'), 
        nullable=False, server_default='NORMAL'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if is_sqlite():
        with op.batch_alter_table('job') as batch_op:
            batch_op.drop_column('type')
    else:
        op.drop_column('job', 'type')
    if is_psql():
         op.get_bind().execute('DROP TYPE "JobTypeEnumType"')

    # ### end Alembic commands ###