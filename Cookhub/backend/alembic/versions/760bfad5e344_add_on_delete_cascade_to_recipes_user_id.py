from alembic import op
import sqlalchemy as sa

# Alembic identifiers
revision = "760bfad5e344"
down_revision = "d9c111b5a395"
branch_labels = None
depends_on = None


def upgrade():
    # Delete previous fk
    op.drop_constraint(
        "recipe_user_id_fkey",
        "recipe",
        type_="foreignkey"
    )

    # Recreate with cascade
    op.create_foreign_key(
        "recipe_user_id_fkey",
        "recipe",
        "user",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint(
        "recipe_user_id_fkey",
        "recipe",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "recipe_user_id_fkey",
        "recipe",
        "user",
        ["user_id"],
        ["id"]
    )
