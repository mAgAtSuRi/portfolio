"""add image_url to recipes

Revision ID: 329063f6e3ce
Revises: 760bfad5e344
Create Date: 2026-03-06 12:23:29.949018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '329063f6e3ce'
down_revision: Union[str, None] = '760bfad5e344'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('recipes', sa.Column('image_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column('recipes', 'image_url')