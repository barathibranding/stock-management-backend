from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Sum


# ============================================================
# BRANCH
# ============================================================

class Branch(models.Model):

    branch_name = models.CharField(
        max_length=150,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["branch_name"]
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.branch_name


# ============================================================
# USER PROFILE
# ============================================================

class UserProfile(models.Model):

    USER_TYPE_CHOICES = [
        ("admin", "Admin"),
        ("staff", "Staff"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    mobile_number = models.CharField(
        max_length=20
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default="staff",
    )

    class Meta:
        ordering = [
            "user__first_name",
            "user__username"
        ]

    def clean(self):
        super().clean()

        if (
            self.user_type == "staff"
            and not self.branch_id
        ):
            raise ValidationError({
                "branch":
                "Branch is required for Staff users."
            })

    def __str__(self):
        return (
            f"{self.user.get_full_name() or self.user.username}"
            f" - {self.user_type}"
        )


# ============================================================
# PRODUCT
# EXISTING PRODUCT MANAGEMENT SYSTEM
# ============================================================

class Product(models.Model):

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="products",
    )

    barcode = models.CharField(
        max_length=150,
        db_index=True,
    )

    short_description = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )

    location = models.CharField(
        max_length=150,
        blank=True,
        default="",
        db_index=True,
    )

    cost_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    selling_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    stk_on_hand = models.IntegerField(
        default=0
    )

    physical_qty = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["barcode"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "branch",
                    "barcode"
                ],
                name="unique_product_barcode_per_branch",
            )
        ]

        indexes = [
            models.Index(
                fields=[
                    "branch",
                    "barcode"
                ]
            ),

            models.Index(
                fields=[
                    "branch",
                    "location"
                ]
            ),
        ]

    @property
    def variance(self):
        return (
            self.physical_qty
            - self.stk_on_hand
        )

    def clean(self):
        super().clean()

        if self.stk_on_hand < 0:
            raise ValidationError({
                "stk_on_hand":
                "Stock on hand cannot be negative."
            })

        if self.physical_qty < 0:
            raise ValidationError({
                "physical_qty":
                "Physical quantity cannot be negative."
            })

        if self.cost_price < 0:
            raise ValidationError({
                "cost_price":
                "Cost price cannot be negative."
            })

        if self.selling_price < 0:
            raise ValidationError({
                "selling_price":
                "Selling price cannot be negative."
            })

    def __str__(self):
        return (
            f"{self.barcode} - "
            f"{self.short_description}"
        )


# ============================================================
# SUPPLIER
# ============================================================

class Supplier(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    supplier_name = models.CharField(
        max_length=255,
        unique=True,
    )

    supplier_location = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active",
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "supplier_name"
        ]

        indexes = [
            models.Index(
                fields=[
                    "supplier_name"
                ]
            ),

            models.Index(
                fields=[
                    "status"
                ]
            ),
        ]

    def __str__(self):
        return self.supplier_name


# ============================================================
# PURCHASE ORDER
# ============================================================

class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("ordered", "Ordered"),
        (
            "partially_received",
            "Partially Received"
        ),
        (
            "fully_received",
            "Fully Received"
        ),
        ("cancelled", "Cancelled"),
    ]

    po_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
    )

    po_date = models.DateField()

    expected_delivery_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="draft",
        db_index=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_purchase_orders",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-created_at"
        ]

        indexes = [
            models.Index(
                fields=[
                    "branch",
                    "status"
                ]
            ),

            models.Index(
                fields=[
                    "supplier",
                    "status"
                ]
            ),

            models.Index(
                fields=[
                    "po_number"
                ]
            ),
        ]

    def __str__(self):
        return self.po_number

    @property
    def total_products(self):
        return self.items.count()

    @property
    def total_quantity(self):
        return (
            self.items.aggregate(
                total=Sum("quantity")
            )["total"] or 0
        )

    @property
    def total_received_quantity(self):
        return (
            self.items.aggregate(
                total=Sum("received_quantity")
            )["total"] or 0
        )

    @property
    def total_amount(self):
        return sum(
            (
                item.total_amount
                for item in self.items.all()
            ),
            0
        )

    @property
    def total_boxes(self):
        return self.containers.count()

    @property
    def total_container_quantity(self):
        return (
            self.containers.aggregate(
                total=Sum("quantity")
            )["total"] or 0
        )


# ============================================================
# PURCHASE ORDER ITEM
# ============================================================

class PurchaseOrderItem(models.Model):

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchase_order_items",
    )

    quantity = models.PositiveIntegerField()

    purchase_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    received_quantity = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "id"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "purchase_order",
                    "product"
                ],
                name="unique_product_per_purchase_order",
            )
        ]

    @property
    def total_amount(self):
        return (
            self.quantity
            * self.purchase_price
        )

    @property
    def pending_quantity(self):
        return max(
            self.quantity
            - self.received_quantity,
            0
        )

    def clean(self):
        super().clean()

        if self.quantity <= 0:
            raise ValidationError({
                "quantity":
                "Quantity must be greater than zero."
            })

        if self.purchase_price < 0:
            raise ValidationError({
                "purchase_price":
                "Purchase price cannot be negative."
            })

        if (
            self.received_quantity
            > self.quantity
        ):
            raise ValidationError({
                "received_quantity":
                "Received quantity cannot exceed ordered quantity."
            })

        if (
            self.purchase_order_id
            and self.product_id
        ):
            if (
                self.product.branch_id
                != self.purchase_order.branch_id
            ):
                raise ValidationError(
                    "Product branch must match Purchase Order branch."
                )

    def __str__(self):
        return (
            f"{self.purchase_order.po_number} - "
            f"{self.product.barcode}"
        )


# ============================================================
# PURCHASE ORDER CONTAINER / BOX
# ============================================================

class PurchaseOrderContainer(models.Model):

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="containers",
    )

    container_number = models.CharField(
        max_length=100,
    )

    container_type = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    remarks = models.TextField(
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "id"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "purchase_order",
                    "container_number"
                ],
                name="unique_container_number_per_po",
            )
        ]

    def clean(self):
        super().clean()

        if self.quantity <= 0:
            raise ValidationError({
                "quantity":
                "Container quantity must be greater than zero."
            })

    def __str__(self):
        return (
            f"{self.purchase_order.po_number} - "
            f"{self.container_number}"
        )


# ============================================================
# PURCHASE RECEIPT
# ============================================================

class PurchaseReceipt(models.Model):

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="receipts",
    )

    receipt_date = models.DateField()

    remarks = models.TextField(
        blank=True,
        default="",
    )

    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="purchase_receipts",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "-receipt_date",
            "-id",
        ]

    def __str__(self):
        return (
            f"Receipt #{self.id} - "
            f"{self.purchase_order.po_number}"
        )

    @property
    def total_quantity(self):
        return (
            self.items.aggregate(
                total=Sum("quantity")
            )["total"] or 0
        )


# ============================================================
# PURCHASE RECEIPT ITEM
# ============================================================

class PurchaseReceiptItem(models.Model):

    receipt = models.ForeignKey(
        PurchaseReceipt,
        on_delete=models.CASCADE,
        related_name="items",
    )

    purchase_order_item = models.ForeignKey(
        PurchaseOrderItem,
        on_delete=models.PROTECT,
        related_name="receipt_items",
    )

    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "id"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "receipt",
                    "purchase_order_item"
                ],
                name="unique_receipt_item",
            )
        ]

    def clean(self):
        super().clean()

        if self.quantity <= 0:
            raise ValidationError({
                "quantity":
                "Received quantity must be greater than zero."
            })

        if self.purchase_order_item_id:

            item = (
                PurchaseOrderItem.objects
                .filter(
                    pk=self.purchase_order_item_id
                )
                .first()
            )

            if item:

                already_received = (
                    PurchaseReceiptItem.objects
                    .filter(
                        purchase_order_item=item
                    )
                    .exclude(
                        pk=self.pk
                    )
                    .aggregate(
                        total=Sum("quantity")
                    )["total"] or 0
                )

                if (
                    already_received
                    + self.quantity
                    > item.quantity
                ):
                    raise ValidationError({
                        "quantity":
                        "Total received quantity cannot exceed ordered quantity."
                    })

    def __str__(self):
        return (
            f"{self.purchase_order_item} - "
            f"{self.quantity}"
        )