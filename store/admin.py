from django.contrib import admin

from .models import (
    Category,
    CustomerProfile,
    Order,
    OrderItem,
    Product,
)


@admin.register(Category)
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


@admin.register(Product)
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


@admin.register(CustomerProfile)
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


@admin.register(Order)
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


@admin.register(OrderItem)
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