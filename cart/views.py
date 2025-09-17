from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from products.models import Product
from .models import CartItem

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    qty = int(request.POST.get("quantity", 1))

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
    )
    # لو موجود زوّد الكمية، لو جديد عيّن الكمية المختارة
    item.quantity = item.quantity + qty if not created else qty
    item.save()

    messages.success(request, f"Added {qty} × “{product.name}” to your cart.")
    return redirect("cart:detail")

@login_required
def detail(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    subtotal = sum(i.line_total for i in items)
    return render(request, "cart/detail.html", {"items": items, "subtotal": subtotal})

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