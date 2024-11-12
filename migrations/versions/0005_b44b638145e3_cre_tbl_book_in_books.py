"""cre tbl book in books

Revision ID: b44b638145e3
Revises: 02001b0bb8f0
Create Date: 2024-11-12 21:11:09.560174

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b44b638145e3'
down_revision: Union[str, None] = '02001b0bb8f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    book = op.create_table('book',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('user_created', sa.Integer(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_modified', sa.Integer(), nullable=True),
    sa.Column('date_modified', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('row_version', sa.BIGINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(('author_id',), ['books.author.id'], ),
    sa.ForeignKeyConstraint(('genre_id',), ['books.genre.id'], ),
    schema='books'
    )


    op.bulk_insert(
        book,
        [
            {'title': 'Мастер и Маргарита',
             'author_id': 1,
             'genre_id': 1,
             'price': 670.99,
             'amount': 3,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'title': 'Белая гвардия',
             'author_id': 1,
             'genre_id': 1,
             'price': 540.50,
             'amount': 5,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'title': 'Идиот',
             'author_id': 2,
             'genre_id': 1,
             'price': 460.00,
             'amount': 10,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'title': 'Братья Карамазовы',
             'author_id': 2,
             'genre_id': 1,
             'price': 799.01,
             'amount': 2,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'title': 'Игрок',
             'author_id': 2,
             'genre_id': 1,
             'price': 480.50,
             'amount': 10,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'title': 'Стихотворения и поэмы',
             'author_id': 3,
             'genre_id': 2,
             'price': 650.00,
             'amount': 15,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'title': 'Черный человек',
             'author_id': 3,
             'genre_id': 2,
             'price': 570.20,
             'amount': 6,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'title': 'Лирика',
             'author_id': 4,
             'genre_id': 2,
             'price': 518.99,
             'amount': 2,
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0}
        ]
    )

def downgrade() -> None:
    op.drop_table('book', schema='books')

