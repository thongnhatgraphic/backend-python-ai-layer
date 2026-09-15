"""enforce memory semantics constraints

Revision ID: 44b7bd9bbbc7
Revises: 4708760ee626
Create Date: 2026-08-17 12:38:57.476165

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "44b7bd9bbbc7"
down_revision: Union[str, Sequence[str], None] = "4708760ee626"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "memories",
        "category",
        existing_type=sa.String(length=100),
        nullable=False,
    )
    op.alter_column(
        "memories",
        "memory_key",
        existing_type=sa.String(length=100),
        nullable=False,
    )
    op.alter_column(
        "memories",
        "cardinality",
        existing_type=sa.String(length=20),
        nullable=False,
    )
    op.alter_column(
        "memories",
        "temporal_behavior",
        existing_type=sa.String(length=20),
        nullable=False,
    )

    op.create_check_constraint(
        "ck_memories_cardinality",
        "memories",
        "cardinality IN ('single', 'multiple')",
    )

    op.create_check_constraint(
        "ck_memories_temporal_behavior",
        "memories",
        """
        temporal_behavior IN (
            'current',
            'historical',
            'event'
        )
        """,
    )

    op.create_index(
        "uq_memories_single_current",
        "memories",
        [
            "user_id",
            "category",
            "memory_key",
        ],
        unique=True,
        postgresql_where=sa.text("""
            cardinality = 'single'
            AND temporal_behavior = 'current'
            """),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "uq_memories_single_current",
        table_name="memories",
    )

    op.drop_constraint(
        "ck_memories_temporal_behavior",
        "memories",
        type_="check",
    )

    op.drop_constraint(
        "ck_memories_cardinality",
        "memories",
        type_="check",
    )

    op.alter_column(
        "memories",
        "temporal_behavior",
        existing_type=sa.String(length=20),
        nullable=True,
    )

    op.alter_column(
        "memories",
        "cardinality",
        existing_type=sa.String(length=20),
        nullable=True,
    )

    op.alter_column(
        "memories",
        "memory_key",
        existing_type=sa.String(length=100),
        nullable=True,
    )

    op.alter_column(
        "memories",
        "category",
        existing_type=sa.String(length=100),
        nullable=True,
    )
