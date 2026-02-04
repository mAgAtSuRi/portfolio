"""Add unit column to ingredients

Revision ID: d9c111b5a395
Revises: f169bc3e5ab8
Create Date: 2026-02-04 21:26:40.279495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd9c111b5a395'
down_revision: Union[str, None] = 'f169bc3e5ab8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'ingredients',
        sa.Column('unit', sa.String(length=10), nullable=False, server_default='g')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_column('ingredients', 'unit')
    # ### end Alembic commands ###
