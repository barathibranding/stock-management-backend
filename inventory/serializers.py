from django.db import transaction

from rest_framework import serializers

from .models import (
    Branch,
    Product,
    Supplier,
    PurchaseOrder,
    PurchaseOrderItem,
    PurchaseOrderContainer,
    PurchaseReceipt,
    PurchaseReceiptItem,
)


# ============================================================
# BRANCH
# ============================================================

class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch

        fields = [
            "id",
            "branch_name",
        ]


# ============================================================
# PRODUCT
# ============================================================

class ProductSerializer(serializers.ModelSerializer):

    branch_name = serializers.CharField(
        source="branch.branch_name",
        read_only=True,
    )

    variance = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Product

        fields = [
            "id",
            "branch",
            "branch_name",
            "barcode",
            "short_description",
            "location",
            "cost_price",
            "selling_price",
            "stk_on_hand",
            "physical_qty",
            "variance",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "branch_name",
            "variance",
            "created_at",
            "updated_at",
        ]

    def validate_barcode(self, value):

        value = str(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Barcode is required."
            )

        return value

    def validate(self, attrs):

        stk = attrs.get(
            "stk_on_hand",
            getattr(
                self.instance,
                "stk_on_hand",
                0
            )
        )

        physical = attrs.get(
            "physical_qty",
            getattr(
                self.instance,
                "physical_qty",
                0
            )
        )

        if stk < 0:
            raise serializers.ValidationError({
                "stk_on_hand":
                "Stock on hand cannot be negative."
            })

        if physical < 0:
            raise serializers.ValidationError({
                "physical_qty":
                "Physical quantity cannot be negative."
            })

        return attrs


# ============================================================
# SUPPLIER
# ============================================================

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier

        fields = [
            "id",
            "supplier_name",
            "supplier_location",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_supplier_name(self, value):

        value = str(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Supplier name is required."
            )

        return value

    def validate_supplier_location(self, value):

        return str(value).strip()


# ============================================================
# PURCHASE ORDER ITEM
# ============================================================

class PurchaseOrderItemSerializer(
    serializers.ModelSerializer
):

    barcode = serializers.CharField(
        source="product.barcode",
        read_only=True,
    )

    short_description = serializers.CharField(
        source="product.short_description",
        read_only=True,
    )

    location = serializers.CharField(
        source="product.location",
        read_only=True,
    )

    product_id = serializers.IntegerField(
        source="product.id",
        read_only=True,
    )

    total_amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True,
    )

    pending_quantity = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = PurchaseOrderItem

        fields = [
            "id",
            "product",
            "product_id",
            "barcode",
            "short_description",
            "location",
            "quantity",
            "purchase_price",
            "total_amount",
            "received_quantity",
            "pending_quantity",
        ]

        read_only_fields = [
            "id",
            "product_id",
            "barcode",
            "short_description",
            "location",
            "total_amount",
            "received_quantity",
            "pending_quantity",
        ]

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )

        return value

    def validate_purchase_price(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Purchase price cannot be negative."
            )

        return value


# ============================================================
# CONTAINER
# ============================================================

class PurchaseOrderContainerSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PurchaseOrderContainer

        fields = [
            "id",
            "container_number",
            "container_type",
            "quantity",
            "remarks",
        ]

        read_only_fields = [
            "id",
        ]

    def validate_container_number(self, value):

        value = str(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Container/Box number is required."
            )

        return value

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Container quantity must be greater than zero."
            )

        return value


# ============================================================
# PURCHASE ORDER LIST SERIALIZER
# ============================================================

class PurchaseOrderListSerializer(
    serializers.ModelSerializer
):

    supplier_name = serializers.CharField(
        source="supplier.supplier_name",
        read_only=True,
    )

    supplier_location = serializers.CharField(
        source="supplier.supplier_location",
        read_only=True,
    )

    branch_name = serializers.CharField(
        source="branch.branch_name",
        read_only=True,
    )

    total_products = serializers.IntegerField(
        read_only=True
    )

    total_quantity = serializers.IntegerField(
        read_only=True
    )

    total_received_quantity = serializers.IntegerField(
        read_only=True
    )

    total_amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True,
    )

    total_boxes = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = PurchaseOrder

        fields = [
            "id",
            "po_number",
            "branch",
            "branch_name",
            "supplier",
            "supplier_name",
            "supplier_location",
            "po_date",
            "expected_delivery_date",
            "status",
            "total_products",
            "total_quantity",
            "total_received_quantity",
            "total_boxes",
            "total_amount",
            "created_at",
            "updated_at",
        ]


# ============================================================
# PURCHASE ORDER DETAIL SERIALIZER
# ============================================================

class PurchaseOrderDetailSerializer(
    serializers.ModelSerializer
):

    supplier_name = serializers.CharField(
        source="supplier.supplier_name",
        read_only=True,
    )

    supplier_location = serializers.CharField(
        source="supplier.supplier_location",
        read_only=True,
    )

    branch_name = serializers.CharField(
        source="branch.branch_name",
        read_only=True,
    )

    items = PurchaseOrderItemSerializer(
        many=True,
        read_only=True,
    )

    containers = PurchaseOrderContainerSerializer(
        many=True,
        read_only=True,
    )

    total_products = serializers.IntegerField(
        read_only=True
    )

    total_quantity = serializers.IntegerField(
        read_only=True
    )

    total_received_quantity = serializers.IntegerField(
        read_only=True
    )

    total_amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True,
    )

    total_boxes = serializers.IntegerField(
        read_only=True
    )

    total_container_quantity = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = PurchaseOrder

        fields = [
            "id",
            "po_number",
            "branch",
            "branch_name",
            "supplier",
            "supplier_name",
            "supplier_location",
            "po_date",
            "expected_delivery_date",
            "status",
            "items",
            "containers",
            "total_products",
            "total_quantity",
            "total_received_quantity",
            "total_boxes",
            "total_container_quantity",
            "total_amount",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "po_number",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        ]


# ============================================================
# PURCHASE ORDER CREATE / UPDATE
# ============================================================

class PurchaseOrderWriteSerializer(
    serializers.Serializer
):

    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.filter(
            status="active"
        )
    )

    po_date = serializers.DateField()

    expected_delivery_date = serializers.DateField(
        required=False,
        allow_null=True,
    )

    branch_id = serializers.IntegerField(
        required=False
    )

    items = PurchaseOrderItemSerializer(
        many=True,
        required=True,
    )

    containers = PurchaseOrderContainerSerializer(
        many=True,
        required=False,
    )

    def validate(self, attrs):

        items = attrs.get(
            "items",
            []
        )

        if not items:
            raise serializers.ValidationError({
                "items":
                "At least one product is required."
            })

        expected_date = attrs.get(
            "expected_delivery_date"
        )

        po_date = attrs.get(
            "po_date"
        )

        if (
            expected_date
            and expected_date < po_date
        ):
            raise serializers.ValidationError({
                "expected_delivery_date":
                "Expected delivery date cannot be before PO date."
            })

        product_ids = [
            item["product"].id
            for item in items
        ]

        if len(product_ids) != len(
            set(product_ids)
        ):
            raise serializers.ValidationError({
                "items":
                "The same product cannot be added twice to one Purchase Order."
            })

        return attrs


# ============================================================
# RECEIPT ITEM
# ============================================================

class PurchaseReceiptItemSerializer(
    serializers.ModelSerializer
):

    product_id = serializers.IntegerField(
        source="purchase_order_item.product.id",
        read_only=True,
    )

    barcode = serializers.CharField(
        source="purchase_order_item.product.barcode",
        read_only=True,
    )

    short_description = serializers.CharField(
        source="purchase_order_item.product.short_description",
        read_only=True,
    )

    ordered_quantity = serializers.IntegerField(
        source="purchase_order_item.quantity",
        read_only=True,
    )

    previous_received_quantity = serializers.IntegerField(
        read_only=True
    )

    pending_quantity = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = PurchaseReceiptItem

        fields = [
            "id",
            "purchase_order_item",
            "product_id",
            "barcode",
            "short_description",
            "ordered_quantity",
            "previous_received_quantity",
            "quantity",
            "pending_quantity",
        ]

        read_only_fields = [
            "id",
            "product_id",
            "barcode",
            "short_description",
            "ordered_quantity",
            "previous_received_quantity",
            "pending_quantity",
        ]


# ============================================================
# RECEIPT DETAIL
# ============================================================

class PurchaseReceiptSerializer(
    serializers.ModelSerializer
):

    items = PurchaseReceiptItemSerializer(
        many=True,
        read_only=True,
    )

    total_quantity = serializers.IntegerField(
        read_only=True
    )

    received_by_name = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseReceipt

        fields = [
            "id",
            "purchase_order",
            "receipt_date",
            "remarks",
            "received_by",
            "received_by_name",
            "items",
            "total_quantity",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "received_by",
            "received_by_name",
            "items",
            "total_quantity",
            "created_at",
        ]

    def get_received_by_name(
        self,
        obj
    ):
        return (
            obj.received_by.get_full_name()
            or obj.received_by.username
        )


# ============================================================
# BULK DELETE
# ============================================================

class BulkDeleteSerializer(
    serializers.Serializer
):

    ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )