"""add user ownership"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "aad3cd142d66"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "followups",
        sa.Column("user_id", sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        "fk_followups_user_id_users",
        "followups",
        "users",
        ["user_id"],
        ["id"]
    )

    op.add_column(
        "leads",
        sa.Column("user_id", sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        "fk_leads_user_id_users",
        "leads",
        "users",
        ["user_id"],
        ["id"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_leads_user_id_users",
        "leads",
        type_="foreignkey"
    )

    op.drop_column("leads", "user_id")

    op.drop_constraint(
        "fk_followups_user_id_users",
        "followups",
        type_="foreignkey"
    )

    op.drop_column("followups", "user_id")
