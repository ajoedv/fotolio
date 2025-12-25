from decimal import Decimal, ROUND_HALF_UP

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django_countries import countries

from products.constants import BASE_SIZE_LABEL
from products.models import Product
from profiles.models import Profile

from .models import CartItem
from .utils import calculate_cart_totals, get_cart_items_for_user
from orders.models import Order, OrderLineItem


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

    profile, _ = Profile.objects.get_or_create(user=request.user)

    session_shipping = request.session.get("checkout_shipping") or {}

    initial_data = {
        "full_name": session_shipping.get("full_name")
        or (profile.shipping_full_name or "").strip(),
        "email": (request.user.email or "").strip(),
        "phone": session_shipping.get("phone")
        or (profile.phone or "").strip(),
        "address1": session_shipping.get("address1")
        or (profile.address_line1 or "").strip(),
        "address2": session_shipping.get("address2")
        or (profile.address_line2 or "").strip(),
        "city": session_shipping.get("city")
        or (profile.city or "").strip(),
        "postcode": session_shipping.get("postcode")
        or (profile.postcode or "").strip(),
        "country": session_shipping.get("country")
        or (str(profile.country) if profile.country else "").strip(),
        "confirm_details": False,
        "save_to_profile": False,
    }

    errors = {}

    if request.method == "POST":
        posted = {
            "full_name": request.POST.get("full_name", "").strip(),
            "email": (request.user.email or "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "address1": request.POST.get("address1", "").strip(),
            "address2": request.POST.get("address2", "").strip(),
            "city": request.POST.get("city", "").strip(),
            "postcode": request.POST.get("postcode", "").strip(),
            "country": request.POST.get("country", "").strip(),
            "confirm_details": bool(request.POST.get("confirm_details")),
            "save_to_profile": bool(request.POST.get("save_to_profile")),
        }

        required_fields = [
            "full_name",
            "email",
            "phone",
            "address1",
            "city",
            "postcode",
            "country",
        ]

        for name in required_fields:
            if not posted.get(name):
                errors[name] = "This field is required."

        if not posted["confirm_details"]:
            errors["confirm_details"] = (
                "Please confirm your order and shipping details."
            )

        if not errors:
            # Save to profile only if user asked for it
            if posted["save_to_profile"]:
                profile.phone = posted["phone"]
                profile.shipping_full_name = posted["full_name"]
                profile.address_line1 = posted["address1"]
                profile.address_line2 = posted["address2"]
                profile.city = posted["city"]
                profile.postcode = posted["postcode"]
                profile.country = posted["country"]  # Country code like "SE"
                profile.save(
                    update_fields=[
                        "phone",
                        "shipping_full_name",
                        "address_line1",
                        "address_line2",
                        "city",
                        "postcode",
                        "country",
                        "updated_at",
                    ]
                )

            # Keep shipping in session for payment step
            request.session["checkout_shipping"] = {
                "full_name": posted["full_name"],
                "email": posted["email"],
                "phone": posted["phone"],
                "address1": posted["address1"],
                "address2": posted["address2"],
                "city": posted["city"],
                "postcode": posted["postcode"],
                "country": posted["country"],
            }
            request.session.modified = True
            return redirect("cart:payment")

        initial_data = posted

    totals = calculate_cart_totals(items)

    context = {
        "items": items,
        "cart_subtotal": totals["subtotal"],
        "cart_tax": totals["tax"],
        "cart_total": totals["total"],
        "base_size": BASE_SIZE_LABEL,
        "form_data": initial_data,
        "errors": errors,
        "country_choices": list(countries),
        "show_shipping_alert": bool(errors),
    }
    return render(request, "cart/checkout.html", context)


@login_required
def payment(request):
    items = get_cart_items_for_user(request.user)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart:detail")

    shipping = request.session.get("checkout_shipping")
    if not shipping:
        messages.error(request, "Please complete checkout before payment.")
        return redirect("cart:checkout")

    country_code = (shipping.get("country") or "").strip()
    country_name = dict(countries).get(country_code, country_code)

    totals = calculate_cart_totals(items)

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

    order = None
    pending_order_id = request.session.get("pending_order_id")

    if pending_order_id:
        try:
            order = Order.objects.get(
                id=pending_order_id,
                user=request.user,
                is_paid=False,
            )
        except Order.DoesNotExist:
            order = None

    if order is None:
        order = Order.objects.create(
            user=request.user,
            full_name=shipping.get("full_name", ""),
            email=shipping.get("email", ""),
            phone=shipping.get("phone", ""),
            address1=shipping.get("address1", ""),
            address2=shipping.get("address2", ""),
            city=shipping.get("city", ""),
            postcode=shipping.get("postcode", ""),
            country=shipping.get("country", ""),
            subtotal=totals["subtotal"],
            tax=totals["tax"],
            total=totals["total"],
            stripe_currency=str(settings.STRIPE_CURRENCY).lower(),
            stripe_amount=amount_ore,
        )

        OrderLineItem.objects.bulk_create(
            [
                OrderLineItem(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    line_total=item.line_total,
                )
                for item in items
            ]
        )

        request.session["pending_order_id"] = order.id
        request.session.modified = True

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_ore,
            currency=settings.STRIPE_CURRENCY,
            automatic_payment_methods={"enabled": True},
            metadata={
                "user_id": str(request.user.id),
                "email": shipping.get("email", ""),
                "order_number": str(order.order_number),
            },
        )
    except Exception:
        messages.error(
            request,
            "Stripe error. Please try again.",
        )
        return redirect("cart:checkout")

    order.stripe_payment_intent_id = intent.id
    order.stripe_currency = str(settings.STRIPE_CURRENCY).lower()
    order.stripe_amount = amount_ore
    order.save(
        update_fields=[
            "stripe_payment_intent_id",
            "stripe_currency",
            "stripe_amount",
            "updated_at",
        ]
    )

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
        "shipping_country_name": country_name,
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
    returned_intent_id = request.GET.get("payment_intent")

    expected_intent_id = request.session.get("expected_payment_intent_id")
    expected_amount = request.session.get("expected_payment_amount")
    expected_currency = request.session.get("expected_payment_currency")

    shipping = request.session.get("checkout_shipping")
    pending_order_id = request.session.get("pending_order_id")

    def go_payment_or_orders():
        if pending_order_id or shipping:
            return redirect("cart:payment")
        return redirect("orders:list")

    if not returned_intent_id:
        messages.info(
            request,
            "Nothing to confirm here. Please check your orders.",
        )
        return redirect("orders:list")

    order = None
    if pending_order_id:
        order = Order.objects.filter(
            id=pending_order_id,
            user=request.user,
        ).first()

    if order is None:
        order = Order.objects.filter(
            user=request.user,
            stripe_payment_intent_id=returned_intent_id,
        ).order_by("-created_at").first()

    if order and order.is_paid:
        request.session.pop("checkout_shipping", None)
        request.session.pop("expected_payment_intent_id", None)
        request.session.pop("expected_payment_amount", None)
        request.session.pop("expected_payment_currency", None)
        request.session.pop("pending_order_id", None)
        request.session.modified = True

        messages.info(request, "This order was already confirmed.")
        return redirect("orders:detail", order_number=order.order_number)

    if expected_intent_id and returned_intent_id != expected_intent_id:
        messages.warning(
            request,
            "Payment verification failed. Please try again.",
        )
        return go_payment_or_orders()

    if not order:
        messages.info(
            request,
            "We couldn't find an order for this payment. "
            "Please check your orders.",
        )
        return redirect("orders:list")

    if expected_amount is None:
        expected_amount = order.stripe_amount
    if expected_currency is None:
        expected_currency = order.stripe_currency

    if expected_amount is None or expected_currency is None:
        messages.info(
            request,
            "Payment session expired. Please check your orders.",
        )
        return redirect("orders:list")

    if not settings.STRIPE_SECRET_KEY:
        messages.info(
            request,
            "Payment already processed. Please check your orders.",
        )
        return redirect("orders:list")

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.retrieve(returned_intent_id)
    except Exception:
        messages.warning(
            request,
            "Could not verify payment right now. Please try again.",
        )
        return go_payment_or_orders()

    if intent.status != "succeeded":
        messages.warning(request, "Payment not completed.")
        return go_payment_or_orders()

    if str(intent.currency).lower() != str(expected_currency).lower():
        messages.warning(request, "Payment currency mismatch.")
        return go_payment_or_orders()

    received = getattr(intent, "amount_received", None) or intent.amount
    if int(received) != int(expected_amount):
        messages.warning(request, "Payment amount mismatch.")
        return go_payment_or_orders()

    if str(intent.metadata.get("user_id", "")) != str(request.user.id):
        messages.warning(request, "Payment user mismatch.")
        return redirect("orders:list")

    order.is_paid = True
    order.stripe_payment_intent_id = returned_intent_id
    order.stripe_currency = str(intent.currency).lower()
    order.stripe_amount = int(received)
    order.save()

    CartItem.objects.filter(user=request.user).delete()

    request.session.pop("checkout_shipping", None)
    request.session.pop("expected_payment_intent_id", None)
    request.session.pop("expected_payment_amount", None)
    request.session.pop("expected_payment_currency", None)
    request.session.pop("pending_order_id", None)
    request.session.modified = True

    messages.success(request, "Your order has been placed successfully.")
    return redirect(
        f"{reverse(
            'orders:detail',
            kwargs={'order_number': order.order_number},
        )}?paid=1"
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
