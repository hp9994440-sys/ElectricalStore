from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from store import views
from store.admin import electrical_store_admin_site


urlpatterns = [

    path(
        "admin/",
        electrical_store_admin_site.urls
    ),

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "product/<slug:slug>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "cart/",
        views.cart_view,
        name="cart"
    ),

    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/update/<int:product_id>/",
        views.update_cart,
        name="update_cart"
    ),

    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "order/success/<str:order_number>/",
        views.order_success,
        name="order_success"
    ),

    path(
        "orders/",
        views.my_orders,
        name="orders"
    ),

    path(
        "order/<str:order_number>/",
        views.order_detail,
        name="order_detail"
    ),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)