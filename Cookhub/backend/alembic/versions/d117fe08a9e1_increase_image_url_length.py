"""increase image_url length

Revision ID: d117fe08a9e1
Revises: 8b47494b6053
Create Date: 2026-03-10 14:19:13.580906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd117fe08a9e1'
down_revision: Union[str, None] = '8b47494b6053'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('recipes', 'image_url', type_=sa.Text())

def downgrade() -> None:
    op.alter_column('recipes', 'image_url', type_=sa.String(500))
    # ### end Alembic commands ###
