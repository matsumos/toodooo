"""create milestones

Revision ID: f66134bbfb2
Revises: 5bff84015db
Create Date: 2012-10-29 22:48:22.180420

"""

# revision identifiers, used by Alembic.
revision = 'f66134bbfb2'
down_revision = '5bff84015db'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'milestones',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False)
    )
    op.add_column('tasks', sa.Column('milestone_id', sa.Integer))


def downgrade():
    op.drop_table('milestones')

