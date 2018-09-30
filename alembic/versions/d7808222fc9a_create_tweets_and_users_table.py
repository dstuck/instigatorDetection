"""Create tweets and users table

Revision ID: d7808222fc9a
Revises: 
Create Date: 2018-09-29 18:21:37.157227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7808222fc9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('screen_name', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.Column('followers_count', sa.BigInteger(), nullable=True),
    sa.Column('favorites_count', sa.BigInteger(), nullable=True),
    sa.Column('statuses_count', sa.BigInteger(), nullable=True),
    sa.Column('lang', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=320), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('db_created_at', sa.DateTime(), nullable=False),
    sa.Column('db_updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('screen_name')
    )
    op.create_table('tweets',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=320), nullable=True),
    sa.Column('lang', sa.String(length=20), nullable=True),
    sa.Column('in_reply_to_tweet_id', sa.BigInteger(), nullable=True),
    sa.Column('in_reply_to_user_id', sa.BigInteger(), nullable=True),
    sa.Column('db_created_at', sa.DateTime(), nullable=False),
    sa.Column('db_updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('tweets')
    op.drop_table('users')

