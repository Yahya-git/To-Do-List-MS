# trunk-ignore(ruff/D400)
# trunk-ignore(ruff/D415)
"""users and verifications table

Revision ID: 858ead8d9679
Revises: 63eea9081df8
Create Date: 2023-05-31 12:36:18.432525

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "858ead8d9679"
down_revision = "63eea9081df8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column(
            "is_verified", sa.Boolean(), server_default=sa.text("FALSE"), nullable=False
        ),
        sa.Column(
            "is_oauth", sa.Boolean(), server_default=sa.text("FALSE"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "verifications",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(
        op.f("ix_verifications_user_id"), "verifications", ["user_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_verifications_user_id"), table_name="verifications")
    op.drop_table("verifications")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
