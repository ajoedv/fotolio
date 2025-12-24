from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order


@login_required
def order_list(request):
    orders = Order.objects.filter(
        user=request.user,
        is_paid=True,
    ).order_by("-created_at")

    context = {"orders": orders}
    return render(request, "orders/order_list.html", context)


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user,
    )

    if not order.is_paid:
        messages.error(request, "This order is not paid yet.")
        return redirect("cart:detail")

    context = {"order": order}
    return render(request, "orders/order_detail.html", context)
