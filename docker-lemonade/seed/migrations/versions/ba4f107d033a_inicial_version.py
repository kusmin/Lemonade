"""Inicial version

Revision ID: ba4f107d033a
Revises: 
Create Date: 2022-02-10 12:07:10.940705

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ba4f107d033a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deployment_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('tag', sa.String(length=100), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deployment_target',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('namespace', sa.String(length=100), nullable=False),
    sa.Column('volume_path', sa.String(length=250), nullable=False),
    sa.Column('description', sa.String(length=400), nullable=True),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.Column('authentication_info', sa.String(length=2500), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('base_service_url', sa.String(length=500), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('target_type', sa.Enum('DOCKER', 'KUBERNETES', 'MARATHON', 'SUPERVISOR', name='DeploymentTargetTypeEnumType'), nullable=False),
    sa.Column('descriptor', mysql.LONGTEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deployment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('internal_name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=400), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('command', sa.String(length=5000), nullable=True),
    sa.Column('workflow_name', sa.String(length=200), nullable=True),
    sa.Column('workflow_id', sa.Integer(), nullable=True),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.Column('model_name', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_login', sa.String(length=100), nullable=False),
    sa.Column('user_name', sa.String(length=100), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('current_status', sa.Enum('ERROR', 'EDITING', 'SAVED', 'RUNNING', 'STOPPED', 'SUSPENDED', 'PENDING', 'DEPLOYED', 'PENDING_UNDEPLOY', 'DEPLOYED_OLD', name='DeploymentStatusEnumType'), nullable=False),
    sa.Column('type', sa.Enum('MODEL', 'DASHBOARD', 'APP', name='DeploymentTypeEnumType'), nullable=False),
    sa.Column('attempts', sa.Integer(), nullable=False),
    sa.Column('log', mysql.LONGTEXT(), nullable=True),
    sa.Column('entry_point', sa.String(length=800), nullable=True),
    sa.Column('replicas', sa.Integer(), nullable=False),
    sa.Column('request_memory', sa.String(length=200), nullable=False),
    sa.Column('limit_memory', sa.String(length=200), nullable=True),
    sa.Column('request_cpu', sa.String(length=20), nullable=True),
    sa.Column('limit_cpu', sa.String(length=20), nullable=True),
    sa.Column('base_service_url', sa.String(length=500), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('extra_parameters', mysql.LONGTEXT(), nullable=True),
    sa.Column('input_spec', mysql.LONGTEXT(), nullable=True),
    sa.Column('output_spec', mysql.LONGTEXT(), nullable=True),
    sa.Column('assets', mysql.LONGTEXT(), nullable=True),
    sa.Column('execution_id', sa.String(length=200), nullable=True),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['deployment_image.id'], name='fk_deployment_image_id'),
    sa.ForeignKeyConstraint(['target_id'], ['deployment_target.id'], name='fk_deployment_target_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deployment_image_id'), 'deployment', ['image_id'], unique=False)
    op.create_index(op.f('ix_deployment_target_id'), 'deployment', ['target_id'], unique=False)
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], name='fk_client_deployment_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_deployment_id'), 'client', ['deployment_id'], unique=False)
    op.create_table('deployment_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('ERROR', 'EDITING', 'SAVED', 'RUNNING', 'STOPPED', 'SUSPENDED', 'PENDING', 'DEPLOYED', 'PENDING_UNDEPLOY', 'DEPLOYED_OLD', name='DeploymentStatusEnumType'), nullable=False),
    sa.Column('log', mysql.LONGTEXT(), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], name='fk_deployment_log_deployment_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deployment_log_deployment_id'), 'deployment_log', ['deployment_id'], unique=False)
    op.create_table('deployment_metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('parameters', sa.String(length=1000), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_login', sa.String(length=100), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], name='fk_deployment_metric_deployment_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deployment_metric_deployment_id'), 'deployment_metric', ['deployment_id'], unique=False)
    op.create_table('metric_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sent_time', sa.DateTime(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('probe_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('data', mysql.LONGTEXT(), nullable=False),
    sa.Column('item', sa.String(length=200), nullable=True),
    sa.Column('sent', sa.String(length=200), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], name='fk_metric_value_deployment_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_metric_value_deployment_id'), 'metric_value', ['deployment_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_metric_value_deployment_id'), table_name='metric_value')
    op.drop_table('metric_value')
    op.drop_index(op.f('ix_deployment_metric_deployment_id'), table_name='deployment_metric')
    op.drop_table('deployment_metric')
    op.drop_index(op.f('ix_deployment_log_deployment_id'), table_name='deployment_log')
    op.drop_table('deployment_log')
    op.drop_index(op.f('ix_client_deployment_id'), table_name='client')
    op.drop_table('client')
    op.drop_index(op.f('ix_deployment_target_id'), table_name='deployment')
    op.drop_index(op.f('ix_deployment_image_id'), table_name='deployment')
    op.drop_table('deployment')
    op.drop_table('deployment_target')
    op.drop_table('deployment_image')
    # ### end Alembic commands ###
