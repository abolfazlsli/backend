"""role requests

Revision ID: c3d1e2f4a5b6
Revises: 86f9c7b9344a
Create Date: 2026-10-08 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d1e2f4a5b6'
down_revision: Union[str, Sequence[str], None] = '86f9c7b9344a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('role_requests',
    sa.Column('partner_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('reviewed_by_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['partner_id'], ['partners.id'], ),
    sa.ForeignKeyConstraint(['reviewed_by_id'], ['partners.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    op.create_index(op.f('ix_role_requests_id'), 'role_requests', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_role_requests_id'), table_name='role_requests')
    op.drop_table('role_requests')
