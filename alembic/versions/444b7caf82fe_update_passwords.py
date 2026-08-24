"""update passwords

Revision ID: 444b7caf82fe
Revises: 024c476312de
Create Date: 2026-08-23 04:50:35.173122
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "444b7caf82fe"
down_revision: Union[str, Sequence[str], None] = "024c476312de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Remove unique constraint from admins.password
    op.drop_constraint(
        op.f("admins_password_key"),
        "admins",
        type_="unique",
    )

    # Add status column temporarily as nullable
    op.add_column(
        "companys",
        sa.Column(
            "status",
            sa.String(),
            nullable=True,
        ),
    )

    # Set existing records to ACTIVE
    op.execute(
        "UPDATE companys SET status = 'ACTIVE'"
    )

    # Make status required
    op.alter_column(
        "companys",
        "status",
        existing_type=sa.String(),
        nullable=False,
    )

    # Remove unique constraint from partners.password
    op.drop_constraint(
        op.f("partners_password_key"),
        "partners",
        type_="unique",
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Restore unique constraint on partners.password
    op.create_unique_constraint(
        op.f("partners_password_key"),
        "partners",
        ["password"],
        postgresql_nulls_not_distinct=False,
    )

    # Remove status column
    op.drop_column(
        "companys",
        "status",
    )

    # Restore unique constraint on admins.password
    op.create_unique_constraint(
        op.f("admins_password_key"),
        "admins",
        ["password"],
        postgresql_nulls_not_distinct=False,
    )