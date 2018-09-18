"""Create initial tables

Revision ID: aaf28961fad2
Revises: 
Create Date: 2018-09-16 19:26:45.087328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaf28961fad2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mentions',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('user_id', sa.BigInteger),
        sa.Column('user_screen_name', sa.String(50)),
        sa.Column('text', sa.Unicode(300)),
        sa.Column('created_at', sa.Integer()),
    )


def downgrade():
    op.drop_table('mentions')

