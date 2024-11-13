"""cre tbl client in books

Revision ID: ccf7df3b3a54
Revises: 20bfe5c49c2b
Create Date: 2024-11-13 09:33:18.732151

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ccf7df3b3a54'
down_revision: Union[str, None] = '20bfe5c49c2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    client = op.create_table('client',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('name_client', sa.String(length=50), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('user_created', sa.Integer(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_modified', sa.Integer(), nullable=True),
    sa.Column('date_modified', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('row_version', sa.BIGINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(('city_id',), ['books.city.id'], ),
    schema='books'
    )

    op.bulk_insert(
        client,
        [
            {'name_client': 'Баранов Павел',
             'city_id': 3,
             'email': 'baranov@test',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_client': 'Абрамова Катя',
             'city_id': 1,
             'email': 'abramova@test',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_client': 'Семенонов Иван',
             'city_id': 2,
             'email': 'semenov@test',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0},
            {'name_client': 'Яковлева Галина',
             'city_id': 1,
             'email': 'yakovleva@test',
             'user_created': 0,
             'date_created': datetime.now(timezone.utc),
             'user_modified': None,
             'date_modified': None,
             'row_version': 0}

        ]
    )


def downgrade() -> None:
    op.drop_table('client', schema='books')

