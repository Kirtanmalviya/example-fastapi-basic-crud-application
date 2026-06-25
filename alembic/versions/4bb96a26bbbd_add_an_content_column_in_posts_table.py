"""add an content column in posts table

Revision ID: 4bb96a26bbbd
Revises: 7019a2cb8ef0
Create Date: 2026-06-25 18:23:07.079566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bb96a26bbbd'
down_revision: Union[str, Sequence[str], None] = '7019a2cb8ef0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
