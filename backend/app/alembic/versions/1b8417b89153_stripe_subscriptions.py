"""Stripe subscriptions

Revision ID: 1b8417b89153
Revises: 9bccec5f4ea9
Create Date: 2023-07-27 18:01:36.604699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1b8417b89153"
down_revision = "9bccec5f4ea9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("order", "checkout_id", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("order", "subscription_id", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("order", "charge_id", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("order", "invoice_url", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("order", "country_code", existing_type=sa.VARCHAR(length=3), nullable=True)
    op.alter_column("order", "country_name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("subscription", "subscription_id", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("subscription", "subscription_id", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("order", "country_name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("order", "country_code", existing_type=sa.VARCHAR(length=3), nullable=False)
    op.alter_column("order", "invoice_url", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("order", "charge_id", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("order", "subscription_id", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("order", "checkout_id", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###
