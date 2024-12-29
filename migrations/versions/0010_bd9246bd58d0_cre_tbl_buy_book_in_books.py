"""cre tbl buy_book in books

Revision ID: bd9246bd58d0
Revises: a6d52c648dd4
Create Date: 2024-11-13 10:12:35.586269

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bd9246bd58d0'
down_revision: Union[str, None] = 'a6d52c648dd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    buy_book = op.create_table('buy_book',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('buy_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('qty', sa.Integer(), nullable=False),
    sa.Column('user_created', sa.Integer(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_modified', sa.Integer(), nullable=True),
    sa.Column('date_modified', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('row_version', sa.BIGINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(('buy_id',), ['books.buy.id'], ),
    sa.ForeignKeyConstraint(('book_id',), ['books.book.id'], ),
    schema='books'
    )

    op.bulk_insert(
        buy_book,
        [
            {'buy_id': 1,
             'book_id': 1,
             'qty': 1,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_id': 1,
             'book_id': 7,
             'qty': 2,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_id': 1,
             'book_id': 3,
             'qty': 1,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_id': 2,
             'book_id': 8,
             'qty': 2,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_id': 3,
             'book_id': 3,
             'qty': 2,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_id': 3,
             'book_id': 2,
             'qty': 1,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_id': 3,
             'book_id': 1,
             'qty': 1,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'buy_id': 4,
             'book_id': 5,
             'qty': 1,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0}
            ]
    )


def downgrade() -> None:
    op.drop_table('buy_book', schema='books')
