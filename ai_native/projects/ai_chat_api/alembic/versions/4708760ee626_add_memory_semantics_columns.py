"""add memory semantics columns

Revision ID: 4708760ee626
Revises: 700d5a0d5589
Create Date: 2026-08-17 11:15:24.204997

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4708760ee626"
down_revision: Union[str, Sequence[str], None] = "700d5a0d5589"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "memories",
        sa.Column("category", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "memories",
        sa.Column("memory_key", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "memories",
        sa.Column("cardinality", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "memories",
        sa.Column("temporal_behavior", sa.String(length=20), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "memories",
        "temporal_behavior",
    )

    op.drop_column(
        "memories",
        "cardinality",
    )

    op.drop_column(
        "memories",
        "memory_key",
    )

    op.drop_column(
        "memories",
        "category",
    )
