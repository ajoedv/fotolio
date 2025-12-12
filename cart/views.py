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
