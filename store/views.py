import uuid

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import LoginForm, RegisterForm, CheckoutForm
from .models import (
    Category,
    CustomerProfile,
    Order,
    OrderItem,
    Product,
)


def home(request):
    categories = Category.objects.filter(
        is_active=True
    )

    products = Product.objects.filter(
        is_active=True
    )

    featured_products = products.filter(
        is_featured=True
    )[:8]

    search_query = request.GET.get("q", "").strip()

    if search_query:
        products = products.filter(
            name__icontains=search_query
        )

    return render(
        request,
        "store/home.html",
        {
            "categories": categories,
            "products": products,
            "featured_products": featured_products,
            "search_query": search_query,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True
    )

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(
        id=product.id
    )[:4]

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()

    return render(
        request,
        "store/login.html",
        {
            "form": form
        }
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            CustomerProfile.objects.create(
                user=user
            )

            login(request, user)

            return redirect("home")
    else:
        form = RegisterForm()

    return render(
        request,
        "store/register.html",
        {
            "form": form
        }
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def cart_view(request):
    cart = request.session.get("cart", {})

    products = Product.objects.filter(
        id__in=cart.keys(),
        is_active=True,
    )

    cart_items = []
    total = 0

    for product in products:
        quantity = int(
            cart.get(str(product.id), 0)
        )

        if quantity <= 0:
            continue

        if quantity > product.stock:
            quantity = product.stock

        if quantity <= 0:
            continue

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "store/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        },
    )


def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    if product.stock <= 0:
        return redirect("product_detail", slug=product.slug)

    cart = request.session.get(
        "cart",
        {}
    )

    product_key = str(product.id)

    current_quantity = int(
        cart.get(product_key, 0)
    )

    if current_quantity < product.stock:
        cart[product_key] = current_quantity + 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def update_cart(request, product_id):
    if request.method != "POST":
        return redirect("cart")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    cart = request.session.get(
        "cart",
        {}
    )

    product_key = str(product_id)

    try:
        quantity = int(
            request.POST.get("quantity", 1)
        )
    except ValueError:
        quantity = 1

    if quantity <= 0:
        cart.pop(product_key, None)

    else:
        quantity = min(
            quantity,
            product.stock
        )

        if quantity > 0:
            cart[product_key] = quantity
        else:
            cart.pop(product_key, None)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = request.session.get(
        "cart",
        {}
    )

    product_key = str(product_id)

    cart.pop(product_key, None)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def checkout(request):
    cart = request.session.get(
        "cart",
        {}
    )

    if not cart:
        return redirect("cart")

    products = Product.objects.filter(
        id__in=cart.keys(),
        is_active=True,
    )

    cart_items = []
    total = 0

    for product in products:
        quantity = int(
            cart.get(str(product.id), 0)
        )

        if quantity <= 0:
            continue

        quantity = min(
            quantity,
            product.stock
        )

        if quantity <= 0:
            continue

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    if not cart_items:
        return redirect("cart")

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():

            with transaction.atomic():

                for item in cart_items:
                    product = Product.objects.select_for_update().get(
                        id=item["product"].id
                    )

                    if product.stock < item["quantity"]:
                        return redirect("cart")

                order_number = (
                    "ORD-"
                    + uuid.uuid4().hex[:10].upper()
                )

                customer = (
                    request.user
                    if request.user.is_authenticated
                    else None
                )

                order = Order.objects.create(
                    customer=customer,
                    order_number=order_number,
                    full_name=form.cleaned_data["full_name"],
                    phone=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                    city=form.cleaned_data["city"],
                    payment_method=form.cleaned_data[
                        "payment_method"
                    ],
                    notes=form.cleaned_data["notes"],
                    total_amount=total,
                )

                for item in cart_items:

                    product = Product.objects.select_for_update().get(
                        id=item["product"].id
                    )

                    quantity = item["quantity"]
                    price = product.price
                    subtotal = price * quantity

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        quantity=quantity,
                        price=price,
                        subtotal=subtotal,
                    )

                    product.stock -= quantity
                    product.save(
                        update_fields=["stock"]
                    )

                request.session["cart"] = {}
                request.session.modified = True

            request.session["last_order_number"] = order.order_number

            return redirect(
                "order_success",
                order_number=order.order_number
            )

    else:
        form = CheckoutForm()

    return render(
        request,
        "store/checkout.html",
        {
            "form": form,
            "cart_items": cart_items,
            "total": total,
        },
    )


def order_success(request, order_number):
    if request.session.get("last_order_number") != order_number:
        return redirect("home")

    order = get_object_or_404(
        Order,
        order_number=order_number,
    )

    request.session.pop("last_order_number", None)

    return render(
        request,
        "store/order_success.html",
        {
            "order": order
        }
    )


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        customer=request.user
    )

    return render(
        request,
        "store/orders.html",
        {
            "orders": orders
        },
    )


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(
        Order,
        order_number=order_number,
        customer=request.user,
    )

    return render(
        request,
        "store/order_detail.html",
        {
            "order": order
        },
    )