"""create tasks table

Revision ID: 19cefeff4786
Revises: None
Create Date: 2012-10-20 08:59:15.556142

"""

# revision identifiers, used by Alembic.
revision = '19cefeff4786'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('doned_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('tasks')
