"""cre tbl city in books

Revision ID: 20bfe5c49c2b
Revises: b44b638145e3
Create Date: 2024-11-13 09:21:47.952952

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20bfe5c49c2b'
down_revision: Union[str, None] = 'b44b638145e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    city = op.create_table('city',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('name_city', sa.String(length=30), nullable=False),
    sa.Column('days_delivery', sa.Integer(), nullable=False),
    sa.Column('user_created', sa.Integer(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_modified', sa.Integer(), nullable=True),
    sa.Column('date_modified', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('row_version', sa.BIGINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='books'
    )

    op.bulk_insert(
        city,
        [
            {'name_city': 'Москва',
             'days_delivery': 5,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_city': 'Санкт-Петербург',
             'days_delivery': 3,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_city': 'Владивосток',
             'days_delivery': 12,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0}
        ]
    )


def downgrade() -> None:
    op.drop_table('city', schema='books')

