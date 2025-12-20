from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product
from products.constants import BASE_SIZE_LABEL

from .models import CartItem
from .utils import get_cart_items_for_user, calculate_cart_totals


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    qty = int(request.POST.get("quantity", 1))

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
    )
    item.quantity = item.quantity + qty if not created else qty
    item.save()

    messages.success(request, f"Added {qty} × “{product.name}” to your cart.")
    return redirect("cart:detail")


@login_required
def detail(request):
    items = get_cart_items_for_user(request.user)
    totals = calculate_cart_totals(items)

    context = {
        "items": items,
        "cart_subtotal": totals["subtotal"],
        "cart_tax": totals["tax"],
        "cart_total": totals["total"],
        "base_size": BASE_SIZE_LABEL,
    }
    return render(request, "cart/detail.html", context)


@login_required
def checkout(request):
    items = get_cart_items_for_user(request.user)

    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart:detail")

    if request.method == "POST":
        if not request.POST.get("confirm_details"):
            messages.error(
                request,
                "Please confirm your order and shipping details.",
            )
            return redirect("cart:checkout")

        request.session["checkout_shipping"] = {
            "full_name": request.POST.get("full_name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "address1": request.POST.get("address1", "").strip(),
            "address2": request.POST.get("address2", "").strip(),
            "city": request.POST.get("city", "").strip(),
            "postcode": request.POST.get("postcode", "").strip(),
            "country": request.POST.get("country", "").strip(),
        }
        request.session.modified = True

        return redirect("cart:payment")

    totals = calculate_cart_totals(items)

    context = {
        "items": items,
        "cart_subtotal": totals["subtotal"],
        "cart_tax": totals["tax"],
        "cart_total": totals["total"],
        "base_size": BASE_SIZE_LABEL,
    }
    return render(request, "cart/checkout.html", context)


@login_required
def payment(request):
    shipping = request.session.get("checkout_shipping")

    if not shipping:
        messages.error(request, "Please complete checkout before payment.")
        return redirect("cart:checkout")

    items = get_cart_items_for_user(request.user)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart:detail")

    totals = calculate_cart_totals(items)

    context = {
        "items": items,
        "shipping": shipping,
        "cart_subtotal": totals["subtotal"],
        "cart_tax": totals["tax"],
        "cart_total": totals["total"],
        "base_size": BASE_SIZE_LABEL,
    }
    return render(request, "cart/payment.html", context)


@login_required
def success(request):
    shipping = request.session.get("checkout_shipping")

    if not shipping:
        messages.error(request, "No order to confirm.")
        return redirect("cart:detail")

    CartItem.objects.filter(
        user=request.user
    ).delete()

    request.session.pop(
        "checkout_shipping",
        None,
    )

    messages.success(
        request,
        "Your order has been placed successfully.",
    )
    return render(
        request,
        "cart/success.html",
    )


@login_required
@require_POST
def update_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    qty = int(request.POST.get("quantity", 1))
    item.quantity = max(1, qty)
    item.save()
    messages.success(request, "Quantity updated.")
    return redirect("cart:detail")


@login_required
@require_POST
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart:detail")
