"""cre tbl buy in books

Revision ID: 3063a7b37f7c
Revises: ccf7df3b3a54
Create Date: 2024-11-13 09:49:58.428693

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3063a7b37f7c'
down_revision: Union[str, None] = 'ccf7df3b3a54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    buy = op.create_table('buy',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('buy_description', sa.String(length=100), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('user_created', sa.Integer(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_modified', sa.Integer(), nullable=True),
    sa.Column('date_modified', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('row_version', sa.BIGINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(('client_id',), ['books.client.id'], ),
    schema='books'
    )

    op.bulk_insert(
        buy,
        [
            {'buy_description': 'Доставка только вечером',
             'client_id': 1,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_description': None,
             'client_id': 3,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_description': 'Упаковать каждую книгу по отдельности',
             'client_id': 2,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_description': None,
             'client_id': 1,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0}
            ]
    )


def downgrade() -> None:
    op.drop_table('buy', schema='books')

