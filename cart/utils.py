from decimal import Decimal

from django.conf import settings

from .models import CartItem


def get_cart_items_for_user(user):
    if not user.is_authenticated:
        return CartItem.objects.none()
    return CartItem.objects.filter(user=user).select_related("product")


def calculate_cart_totals(items):
    gross_total = sum(
        (item.line_total for item in items),
        Decimal("0.00"),
    )

    vat_rate = getattr(settings, "VAT_RATE", Decimal("0.00"))

    if vat_rate > Decimal("0.00"):
        divisor = Decimal("1.00") + vat_rate
        net_total = (gross_total / divisor).quantize(Decimal("0.01"))
        tax_amount = (gross_total - net_total).quantize(Decimal("0.01"))
    else:
        net_total = gross_total
        tax_amount = Decimal("0.00")

    return {
        "subtotal": net_total,
        "tax": tax_amount,
        "total": gross_total,
    }
