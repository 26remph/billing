"""empty message

Revision ID: aea01a961fcc
Revises: 
Create Date: 2023-12-17 04:02:26.043630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aea01a961fcc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "cart",
        sa.Column("cartId", sa.String(length=255), nullable=True),
        sa.Column("externalId", sa.String(length=255), nullable=True),
        sa.Column("total", sa.Float(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__cart")),
    )
    op.create_table(
        "item_quantity",
        sa.Column("available", sa.Float(), nullable=True),
        sa.Column("count", sa.Float(), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__item_quantity")),
    )
    op.create_table(
        "item",
        sa.Column("productId", sa.Uuid(), nullable=False),
        sa.Column("item_quantity_id", sa.Uuid(), nullable=False),
        sa.Column("discountedUnitPrice", sa.Float(), nullable=True),
        sa.Column("finalPrice", sa.Float(), nullable=True),
        sa.Column("subtotal", sa.Float(), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("total", sa.Float(), nullable=True),
        sa.Column("type", sa.Enum("PHYSICAL", "DIGITAL", "UNSPECIFIED", name="itemtype"), nullable=False),
        sa.Column("unitPrice", sa.Float(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["item_quantity_id"],
            ["item_quantity.id"],
            name=op.f("fk__item__item_quantity_id__item_quantity"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__item")),
    )
    op.create_table(
        "order",
        sa.Column("cart_id", sa.Uuid(), nullable=False),
        sa.Column("currencyCode", sa.Enum("RUB", name="currencycode"), nullable=False),
        sa.Column("merchantId", sa.Uuid(), nullable=True),
        sa.Column("orderAmount", sa.Float(), nullable=True),
        sa.Column("orderId", sa.Uuid(), nullable=True),
        sa.Column(
            "paymentStatus",
            sa.Enum(
                "PENDING",
                "AUTHORIZED",
                "CAPTURED",
                "VOIDED",
                "REFUNDED",
                "PARTIALLY_REFUNDED",
                "FAILED",
                "null",
                name="paymentstatus",
            ),
            nullable=True,
        ),
        sa.Column("paymentUrl", sa.Text(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["cart_id"], ["cart.id"], name=op.f("fk__order__cart_id__cart"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__order")),
    )
    op.create_table(
        "cart_item",
        sa.Column("cart_id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["cart_id"], ["cart.id"], name=op.f("fk__cart_item__cart_id__cart"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["item_id"], ["item.id"], name=op.f("fk__cart_item__item_id__item"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__cart_item")),
    )
    op.create_table(
        "operation",
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("approvalCode", sa.String(length=255), nullable=True),
        sa.Column("externalOperationId", sa.String(length=255), nullable=True),
        sa.Column("operationId", sa.Uuid(), nullable=False),
        sa.Column(
            "operationType",
            sa.Enum("AUTHORIZE", "REFUND", "CAPTURE", "VOID", "RECURRING", name="operationtype"),
            nullable=False,
        ),
        sa.Column("orderId", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("status", sa.Enum("PENDING", "SUCCESS", "FAIL", name="operationstatus"), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["orderId"], ["order.id"], name=op.f("fk__operation__orderId__order"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__operation")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("operation")
    op.drop_table("cart_item")
    op.drop_table("order")
    op.drop_table("item")
    op.drop_table("item_quantity")
    op.drop_table("cart")
    # ### end Alembic commands ###
