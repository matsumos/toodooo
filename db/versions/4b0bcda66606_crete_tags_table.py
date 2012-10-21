"""crete tags table

Revision ID: 4b0bcda66606
Revises: 19cefeff4786
Create Date: 2012-10-21 16:56:33.476139

"""

# revision identifiers, used by Alembic.
revision = '4b0bcda66606'
down_revision = '19cefeff4786'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False)
    )


def downgrade():
    op.drop_table('tags')
