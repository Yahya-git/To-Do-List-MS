# trunk-ignore(ruff/D400)
# trunk-ignore(ruff/D415)
"""added file_name column to attachments table

Revision ID: ba92b48a6dd1
Revises: 1da97c81acd7
Create Date: 2023-03-29 16:26:49.645588

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "ba92b48a6dd1"
down_revision = "1da97c81acd7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("attachments", sa.Column("file_name", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("attachments", "file_name")
    # ### end Alembic commands ###
