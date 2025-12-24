from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from products.models import Product


class Order(models.Model):

    order_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True,
        blank=True,
    )

    order_year = models.PositiveSmallIntegerField(
        editable=False,
        null=True,
        blank=True,
        db_index=True,
    )

    order_seq = models.PositiveIntegerField(
        editable=False,
        null=True,
        blank=True,
        db_index=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)

    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120)
    postcode = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=120)

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
    )
    stripe_currency = models.CharField(
        max_length=10,
        blank=True,
    )
    stripe_amount = models.IntegerField(
        default=0,
    )

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["order_year", "order_seq"],
                name="uniq_order_year_seq",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.order_number:
            with transaction.atomic():
                year = timezone.now().year
                last = (
                    Order.objects.select_for_update()
                    .filter(order_year=year)
                    .order_by("-order_seq")
                    .first()
                )
                next_seq = (last.order_seq + 1) if last else 1
                self.order_year = year
                self.order_seq = next_seq
                self.order_number = f"FO-{year}-{next_seq:06d}"
                super().save(*args, **kwargs)
                return
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    product_name = models.CharField(
        max_length=255,
    )

    quantity = models.PositiveIntegerField(default=1)

    line_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
