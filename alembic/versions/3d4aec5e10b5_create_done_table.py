"""create done table

Revision ID: 3d4aec5e10b5
Revises: 1b2c6291c2a2
Create Date: 2024-10-04 06:31:40.075211

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3d4aec5e10b5"
down_revision: Union[str, None] = "1b2c6291c2a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dones",
        sa.Column("id", sa.Integer, nullable=False),
    )

    op.create_foreign_key(
        "done_tasks_fk",
        source_table="dones",
        referent_table="tasks",
        local_cols=["id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("done_tasks_fk", table_name="dones", type_="foreignkey")
    op.drop_table("dones")
