"""cre_tbl_author_in_books

Revision ID: 02001b0bb8f0
Revises: 51c57f9d66df
Create Date: 2024-11-12 19:43:06.308031

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '02001b0bb8f0'
down_revision: Union[str, None] = '51c57f9d66df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    author = op.create_table('author',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('name_author', sa.String(), nullable=False),
    sa.Column('user_created', sa.Integer(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_modified', sa.Integer(), nullable=True),
    sa.Column('date_modified', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('row_version', sa.BIGINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='books'
    )

    op.bulk_insert(
        author,
        [
            {'name_author': 'Булгаков М.А.',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_author': 'Достоевский Ф.М.',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_author': 'Есенин С.А.',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_author': 'Пастернак Б.Л.',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_author': 'Лермонтов М.Ю.',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0}
        ]
    )


def downgrade() -> None:
    op.drop_table('author', schema='books')

