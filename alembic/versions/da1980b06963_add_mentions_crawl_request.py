"""add mentions crawl request

Revision ID: da1980b06963
Revises: 2821701f8172
Create Date: 2018-10-28 16:33:27.787633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da1980b06963'
down_revision = '2821701f8172'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('mentions_crawl_request',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('mentioned_screen_name', sa.String(length=50), nullable=True),
    sa.Column('first_id', sa.BigInteger(), nullable=True),
    sa.Column('last_id', sa.BigInteger(), nullable=True),
    sa.Column('in_process', sa.Boolean(), nullable=True),
    sa.Column('recurring', sa.Boolean(), nullable=True),
    sa.Column('last_fulfilled', sa.DateTime(), nullable=True),
    sa.Column('db_created_at', sa.DateTime(), nullable=False),
    sa.Column('db_updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('mentions_crawl_request')
