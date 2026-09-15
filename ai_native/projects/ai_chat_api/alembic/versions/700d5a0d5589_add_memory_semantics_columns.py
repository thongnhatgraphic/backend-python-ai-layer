"""Add memory semantics columns

Revision ID: 700d5a0d5589
Revises: 7185a45ecb9d
Create Date: 2026-08-17 11:14:53.843141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '700d5a0d5589'
down_revision: Union[str, Sequence[str], None] = '7185a45ecb9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
