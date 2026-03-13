"""add number_of_persons to recipes

Revision ID: 8b47494b6053
Revises: 329063f6e3ce
Create Date: 2026-03-09 12:06:09.862125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '8b47494b6053'
down_revision: Union[str, None] = '329063f6e3ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('recipes', sa.Column('number_of_persons', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('recipes', 'number_of_persons')