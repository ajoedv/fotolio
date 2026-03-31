from decimal import Decimal

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from cart.context_processors import cart_summary
from cart.models import CartItem
from products.models import Product


class CartContextProcessorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password="testpass123",
        )
        self.product = Product.objects.create(
            name="Sunset Print",
            description="Beautiful sunset artwork.",
            price=Decimal("49.99"),
        )

    def test_anonymous_user_gets_zero_cart_summary(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()

        context = cart_summary(request)

        self.assertEqual(context["cart_count"], 0)
        self.assertEqual(context["cart_total"], 0)

    def test_authenticated_user_with_empty_cart_gets_zero_summary(self):
        request = self.factory.get("/")
        request.user = self.user

        context = cart_summary(request)

        self.assertEqual(context["cart_count"], 0)
        self.assertEqual(context["cart_total"], 0)

    def test_authenticated_user_gets_correct_cart_summary(self):
        CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
        )
        CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
        )

        request = self.factory.get("/")
        request.user = self.user

        context = cart_summary(request)

        self.assertEqual(context["cart_count"], 3)
        self.assertEqual(context["cart_total"], Decimal("149.97"))
