"""Foreign key concept for data source

Revision ID: 0c56a2478a23
Revises: 7fd1bcffbbc2
Create Date: 2020-05-11 15:45:20.757418

"""
from alembic import op
import sqlalchemy as sa
from limonero.migration_utils import is_psql, is_sqlite

# revision identifiers, used by Alembic.
revision = '0c56a2478a23'
down_revision = '7fd1bcffbbc2'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_source_foreign_key',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_source_id', sa.Integer(), nullable=False),
    sa.Column('to_source_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['from_source_id'], ['data_source.id'], ),
    sa.ForeignKeyConstraint(['to_source_id'], ['data_source.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attribute_foreign_key',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('direction', sa.Enum('FROM', 'TO', name='AttributeForeignKeyDirectionEnumType'), nullable=False),
    sa.Column('foreign_key_id', sa.Integer(), nullable=False),
    sa.Column('from_attribute_id', sa.Integer(), nullable=False),
    sa.Column('to_attribute_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['foreign_key_id'], ['data_source_foreign_key.id'], ),
    sa.ForeignKeyConstraint(['from_attribute_id'], ['attribute.id'], ),
    sa.ForeignKeyConstraint(['to_attribute_id'], ['attribute.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    if is_sqlite():
        with op.batch_alter_table('attribute') as batch_op:
            batch_op.add_column(sa.Column('key', sa.Boolean(), nullable=False, server_default='false'))
    else:
        op.add_column('attribute', sa.Column('key', sa.Boolean(), nullable=False))
    ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if is_sqlite():
        with op.batch_alter_table('attribute') as batch_op:
            batch_op.drop_column('key')
    else: 
        op.drop_column('attribute', 'key')

    op.drop_table('attribute_foreign_key')
    op.drop_table('data_source_foreign_key')

    if is_psql():
        op.get_bind().execute('DROP TYPE "AttributeForeignKeyDirectionEnumType"')

    # ### end Alembic commands ###
