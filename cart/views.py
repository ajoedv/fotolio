from decimal import Decimal, ROUND_HALF_UP

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from products.constants import BASE_SIZE_LABEL
from products.models import Product

from .models import CartItem
from .utils import calculate_cart_totals, get_cart_items_for_user


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

    messages.success(
        request,
        f"Added {qty} × “{product.name}” to your cart.",
    )
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

    # Ensure total is exactly 2 decimals before converting to öre
    total_kr = Decimal(str(totals["total"])).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    amount_ore = int(
        (total_kr * Decimal("100")).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )
    )

    if not settings.STRIPE_SECRET_KEY or not settings.STRIPE_PUBLIC_KEY:
        messages.error(
            request,
            "Stripe keys are missing. Please check your settings.",
        )
        return redirect("cart:checkout")

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_ore,
            currency=settings.STRIPE_CURRENCY,
            automatic_payment_methods={"enabled": True},
            metadata={
                "user_id": str(request.user.id),
                "email": shipping.get("email", ""),
            },
        )
    except Exception:
        messages.error(
            request,
            "Stripe error. Please try again.",
        )
        return redirect("cart:checkout")

    # Store expected intent + amount/currency in session
    # for server-side verification
    request.session["expected_payment_intent_id"] = intent.id
    request.session["expected_payment_amount"] = amount_ore
    request.session["expected_payment_currency"] = str(
        settings.STRIPE_CURRENCY
    ).lower()
    request.session.modified = True

    success_url = request.build_absolute_uri(reverse("cart:success"))

    context = {
        "items": items,
        "shipping": shipping,
        "cart_subtotal": totals["subtotal"],
        "cart_tax": totals["tax"],
        "cart_total": totals["total"],
        "base_size": BASE_SIZE_LABEL,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": intent.client_secret,
        "success_url": success_url,
    }
    return render(request, "cart/payment.html", context)


@login_required
def success(request):
    shipping = request.session.get("checkout_shipping")
    if not shipping:
        messages.error(request, "No order to confirm.")
        return redirect("cart:detail")

    expected_intent_id = request.session.get("expected_payment_intent_id")
    expected_amount = request.session.get("expected_payment_amount")
    expected_currency = request.session.get("expected_payment_currency")

    returned_intent_id = request.GET.get("payment_intent")

    # Block manual access
    if not expected_intent_id or not returned_intent_id:
        messages.error(request, "Payment not verified.")
        return redirect("cart:payment")

    if returned_intent_id != expected_intent_id:
        messages.error(request, "Payment verification failed.")
        return redirect("cart:payment")

    # Ensure we have verification data
    if expected_amount is None or expected_currency is None:
        messages.error(request, "Payment verification data missing.")
        return redirect("cart:payment")

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.retrieve(returned_intent_id)
    except Exception:
        messages.error(
            request,
            "Could not verify payment. Please try again.",
        )
        return redirect("cart:payment")

    if intent.status != "succeeded":
        messages.error(request, "Payment not completed.")
        return redirect("cart:payment")

    # Verify currency (case-insensitive)
    if str(intent.currency).lower() != str(expected_currency).lower():
        messages.error(request, "Payment currency mismatch.")
        return redirect("cart:payment")

    # Verify amount
    received = getattr(intent, "amount_received", None) or intent.amount
    if int(received) != int(expected_amount):
        messages.error(request, "Payment amount mismatch.")
        return redirect("cart:payment")

    # Verify this payment belongs to the current user
    if str(intent.metadata.get("user_id", "")) != str(request.user.id):
        messages.error(request, "Payment user mismatch.")
        return redirect("cart:payment")

    # Payment verified
    CartItem.objects.filter(user=request.user).delete()

    # Clear checkout session data
    request.session.pop("checkout_shipping", None)
    request.session.pop("expected_payment_intent_id", None)
    request.session.pop("expected_payment_amount", None)
    request.session.pop("expected_payment_currency", None)
    request.session.modified = True

    messages.success(request, "Your order has been placed successfully.")
    return render(request, "cart/success.html")


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
