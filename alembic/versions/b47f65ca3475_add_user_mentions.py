"""Add user mentions

Revision ID: b47f65ca3475
Revises: d7808222fc9a
Create Date: 2018-09-29 19:21:14.292104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b47f65ca3475'
down_revision = 'd7808222fc9a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tweet_mentions',
    sa.Column('tweet_id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('tweet_id', 'user_id')
    )


def downgrade():
    op.drop_table('tweet_mentions')

