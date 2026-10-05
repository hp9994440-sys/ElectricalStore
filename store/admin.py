from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import (
    Category,
    CustomerProfile,
    Order,
    OrderItem,
    Product,
)


class ElectricalStoreAdminSite(AdminSite):
    site_header = "Electrical Store Administration"
    site_title = "Electrical Store Admin"
    index_title = "Store Dashboard"
    index_template = "admin/custom_index.html"

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        extra_context["pending_orders_count"] = Order.objects.filter(
            status="pending"
        ).count()

        return super().index(
            request,
            extra_context=extra_context
        )


electrical_store_admin_site = ElectricalStoreAdminSite(
    name="electrical_store_admin"
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "is_active",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "sku",
        "price",
        "wholesale_price",
        "stock",
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "sku",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone",
        "city",
    )

    search_fields = (
        "user__username",
        "phone",
        "city",
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "customer",
        "full_name",
        "city",
        "payment_method",
        "status",
        "total_amount",
        "created_at",
    )

    search_fields = (
        "order_number",
        "full_name",
        "phone",
        "customer__username",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    ordering = (
        "-created_at",
    )


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product_name",
        "quantity",
        "price",
        "subtotal",
    )

    search_fields = (
        "product_name",
        "order__order_number",
    )


electrical_store_admin_site.register(
    Category,
    CategoryAdmin
)

electrical_store_admin_site.register(
    Product,
    ProductAdmin
)

electrical_store_admin_site.register(
    CustomerProfile,
    CustomerProfileAdmin
)

electrical_store_admin_site.register(
    Order,
    OrderAdmin
)

electrical_store_admin_site.register(
    OrderItem,
    OrderItemAdmin
)