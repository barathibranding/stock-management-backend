from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    MeView,

    BranchListView,
    BranchSelectView,
    BranchDetailsView,

    ProductListCreateView,
    ProductDetailView,
    ProductBulkDeleteView,
    ProductBulkImportView,
    ProductExportView,

    SupplierListCreateView,
    SupplierDetailView,
    SupplierStatusView,

    PurchaseOrderProductSearchView,

    PurchaseOrderListView,
    PurchaseOrderCreateView,
    PurchaseOrderDetailView,
    PurchaseOrderUpdateView,

    PurchaseOrderOrderView,
    PurchaseOrderCancelView,

    PurchaseOrderReceiveView,
    PurchaseOrderReceivingHistoryView,
)


urlpatterns = [

    # ========================================================
    # AUTH
    # ========================================================

    path(
        "auth/login/",
        LoginView.as_view(),
        name="api-login",
    ),

    path(
        "auth/logout/",
        LogoutView.as_view(),
        name="api-logout",
    ),

    path(
        "auth/me/",
        MeView.as_view(),
        name="api-me",
    ),


    # ========================================================
    # BRANCH
    # ========================================================

    path(
        "branches/",
        BranchListView.as_view(),
        name="branch-list",
    ),

    path(
        "branches/select/",
        BranchSelectView.as_view(),
        name="branch-select",
    ),

    path(
        "branch-details/",
        BranchDetailsView.as_view(),
        name="branch-details",
    ),


    # ========================================================
    # PRODUCTS
    # ========================================================

    path(
        "products/",
        ProductListCreateView.as_view(),
        name="product-list-create",
    ),

    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),

    path(
        "products/bulk-delete/",
        ProductBulkDeleteView.as_view(),
        name="product-bulk-delete",
    ),

    path(
        "products/bulk-import/",
        ProductBulkImportView.as_view(),
        name="product-bulk-import",
    ),

    path(
        "products/export/",
        ProductExportView.as_view(),
        name="product-export",
    ),


    # ========================================================
    # SUPPLIERS
    # ========================================================

    path(
        "suppliers/",
        SupplierListCreateView.as_view(),
        name="supplier-list-create",
    ),

    path(
        "suppliers/<int:pk>/",
        SupplierDetailView.as_view(),
        name="supplier-detail",
    ),

    path(
        "suppliers/<int:pk>/status/",
        SupplierStatusView.as_view(),
        name="supplier-status",
    ),


    # ========================================================
    # PURCHASE ORDER PRODUCT SEARCH
    # ========================================================

    path(
        "purchase-orders/products/search/",
        PurchaseOrderProductSearchView.as_view(),
        name="purchase-order-product-search",
    ),


    # ========================================================
    # PURCHASE ORDERS
    # ========================================================

    path(
        "purchase-orders/",
        PurchaseOrderListView.as_view(),
        name="purchase-order-list",
    ),

    path(
        "purchase-orders/create/",
        PurchaseOrderCreateView.as_view(),
        name="purchase-order-create",
    ),

    path(
        "purchase-orders/<int:pk>/",
        PurchaseOrderDetailView.as_view(),
        name="purchase-order-detail",
    ),

    path(
        "purchase-orders/<int:pk>/update/",
        PurchaseOrderUpdateView.as_view(),
        name="purchase-order-update",
    ),

    path(
        "purchase-orders/<int:pk>/order/",
        PurchaseOrderOrderView.as_view(),
        name="purchase-order-order",
    ),

    path(
        "purchase-orders/<int:pk>/cancel/",
        PurchaseOrderCancelView.as_view(),
        name="purchase-order-cancel",
    ),


    # ========================================================
    # PURCHASE RECEIVING
    # ========================================================

    path(
        "purchase-orders/<int:pk>/receive/",
        PurchaseOrderReceiveView.as_view(),
        name="purchase-order-receive",
    ),

    path(
        "purchase-orders/<int:pk>/receiving-history/",
        PurchaseOrderReceivingHistoryView.as_view(),
        name="purchase-order-receiving-history",
    ),
]