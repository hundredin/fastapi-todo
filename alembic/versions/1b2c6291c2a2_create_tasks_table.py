"""create tasks table

Revision ID: 1b2c6291c2a2
Revises: 
Create Date: 2024-10-04 06:25:53.535444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b2c6291c2a2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String),
        sa.Column('due_date', sa.Date)
    )


def downgrade() -> None:
    op.drop_table('tasks')
