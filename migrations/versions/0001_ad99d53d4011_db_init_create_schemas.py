"""db init, create schemas

Revision ID: ad99d53d4011
Revises: 
Create Date: 2024-10-29 13:18:01.253891

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ad99d53d4011'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create schema users")
    op.execute("create schema books")


def downgrade() -> None:
    op.execute("drop schema users")
    op.execute("drop schema books")
