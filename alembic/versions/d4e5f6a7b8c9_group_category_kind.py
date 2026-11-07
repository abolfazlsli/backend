"""group category kind

Revision ID: d4e5f6a7b8c9
Revises: c3d1e2f4a5b6
Create Date: 2026-10-08 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c3d1e2f4a5b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('group_category', sa.Column('kind', sa.String(), nullable=True))
    op.create_index(op.f('ix_group_category_kind'), 'group_category', ['kind'], unique=False)
    # گروه‌های قبلی همه گروه درسی بودن
    op.execute("UPDATE group_category SET kind = 'subject' WHERE kind IS NULL")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_group_category_kind'), table_name='group_category')
    op.drop_column('group_category', 'kind')
