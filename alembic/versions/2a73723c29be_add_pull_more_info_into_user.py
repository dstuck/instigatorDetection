"""add pull more info into user

Revision ID: 2a73723c29be
Revises: da1980b06963
Create Date: 2018-10-28 17:32:03.545951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a73723c29be'
down_revision = 'da1980b06963'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('friends_count', sa.BigInteger(), nullable=True))
    op.add_column('users', sa.Column('protected', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('verified', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('users', 'verified')
    op.drop_column('users', 'protected')
    op.drop_column('users', 'friends_count')
