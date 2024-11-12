"""cre tbl user in users

Revision ID: 7003f2ab7894
Revises: ad99d53d4011
Create Date: 2024-10-29 22:06:58.773273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7003f2ab7894'
down_revision: Union[str, None] = 'ad99d53d4011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('user_created', sa.Integer(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_modified', sa.Integer(), nullable=True),
    sa.Column('date_modified', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('row_version', sa.BIGINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='users'
    )
    op.create_index(op.f('ix_users_user_email'), 'user', ['email'], unique=True, schema='users')


def downgrade() -> None:
    op.drop_index(op.f('ix_users_user_email'), table_name='user', schema='users')
    op.drop_table('user', schema='users')

