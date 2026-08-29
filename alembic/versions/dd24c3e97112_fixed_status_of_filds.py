"""fixed status of filds

Revision ID: dd24c3e97112
Revises: c99abd773cf1
Create Date: 2026-08-26 05:28:59.110586
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "dd24c3e97112"
down_revision: Union[str, Sequence[str], None] = "c99abd773cf1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # -----------------------------
    # Create status enum
    # -----------------------------
    status_enum = postgresql.ENUM(
        "ACTIVE",
        "DISACTIVE",
        name="statusenum",
    )

    status_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    # -----------------------------
    # Add status to filds
    # -----------------------------
    op.add_column(
        "filds",
        sa.Column(
            "status",
            status_enum,
            nullable=False,
            server_default="ACTIVE",
        ),
    )

    # -----------------------------
    # Add status to instances
    # -----------------------------
    op.add_column(
        "instances",
        sa.Column(
            "status",
            status_enum,
            nullable=False,
            server_default="ACTIVE",
        ),
    )

    # -----------------------------
    # Remove old columns
    # -----------------------------
    op.drop_column(
        "instances",
        "order",
    )

    op.drop_column(
        "instances",
        "required",
    )

    # -----------------------------
    # Remove default after migration
    # -----------------------------
    op.alter_column(
        "filds",
        "status",
        server_default=None,
    )

    op.alter_column(
        "instances",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    # -----------------------------
    # Restore old columns
    # -----------------------------
    op.add_column(
        "instances",
        sa.Column(
            "required",
            sa.BOOLEAN(),
            nullable=True,
        ),
    )

    op.add_column(
        "instances",
        sa.Column(
            "order",
            sa.INTEGER(),
            nullable=True,
        ),
    )

    # -----------------------------
    # Remove status columns
    # -----------------------------
    op.drop_column(
        "instances",
        "status",
    )

    op.drop_column(
        "filds",
        "status",
    )

    # -----------------------------
    # Drop enum
    # -----------------------------
    status_enum = postgresql.ENUM(
        "ACTIVE",
        "DISACTIVE",
        name="statusenum",
    )

    status_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )