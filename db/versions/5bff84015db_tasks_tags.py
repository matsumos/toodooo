"""tasks_tags

Revision ID: 5bff84015db
Revises: 4b0bcda66606
Create Date: 2012-10-26 20:57:31.573143

"""

# revision identifiers, used by Alembic.
revision = '5bff84015db'
down_revision = '4b0bcda66606'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'tasks_tags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.Integer),
        sa.Column('tag_id', sa.Integer)
    )


def downgrade():
    op.drop_table('tasks_tags')
