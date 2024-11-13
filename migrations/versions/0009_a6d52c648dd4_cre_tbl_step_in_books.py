"""cre tbl step in books

Revision ID: a6d52c648dd4
Revises: 3063a7b37f7c
Create Date: 2024-11-13 10:01:32.671967

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a6d52c648dd4'
down_revision: Union[str, None] = '3063a7b37f7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    step = op.create_table('step',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('name_step', sa.String(length=30), nullable=False),
    sa.Column('user_created', sa.Integer(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_modified', sa.Integer(), nullable=True),
    sa.Column('date_modified', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('row_version', sa.BIGINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='books'
    )

    op.bulk_insert(
        step,
        [
            {'name_step': 'Оплата',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_step': 'Упаковка',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_step': 'Транспортировка',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_step': 'Доставка',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0}
            ]
    )


def downgrade() -> None:
    op.drop_table('step', schema='books')

