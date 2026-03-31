from decimal import Decimal

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, override_settings

from cart.models import CartItem
from cart.utils import calculate_cart_totals, get_cart_items_for_user
from products.models import Product


class CartUtilsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        self.product = Product.objects.create(
            name="Sunset Print",
            description="Beautiful sunset artwork.",
            price=Decimal("49.99"),
        )

    def test_get_cart_items_for_anonymous_user_returns_none_queryset(self):
        user = AnonymousUser()

        items = get_cart_items_for_user(user)

        self.assertEqual(items.count(), 0)

    def test_get_cart_items_for_authenticated_user_returns_only_their_items(
        self,
    ):
        user_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
        )
        CartItem.objects.create(
            user=self.other_user,
            product=self.product,
            quantity=1,
        )

        items = get_cart_items_for_user(self.user)

        self.assertEqual(items.count(), 1)
        self.assertEqual(items.first(), user_item)

    @override_settings(VAT_RATE=Decimal("0.00"))
    def test_calculate_cart_totals_without_vat(self):
        item_one = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
        )
        item_two = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
        )

        totals = calculate_cart_totals([item_one, item_two])

        self.assertEqual(totals["subtotal"], Decimal("149.97"))
        self.assertEqual(totals["tax"], Decimal("0.00"))
        self.assertEqual(totals["total"], Decimal("149.97"))

    @override_settings(VAT_RATE=Decimal("0.25"))
    def test_calculate_cart_totals_with_vat(self):
        item_one = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
        )
        item_two = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
        )

        totals = calculate_cart_totals([item_one, item_two])

        self.assertEqual(totals["subtotal"], Decimal("119.98"))
        self.assertEqual(totals["tax"], Decimal("29.99"))
        self.assertEqual(totals["total"], Decimal("149.97"))
