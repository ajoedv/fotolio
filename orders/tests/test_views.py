from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from orders.models import Order


class OrderViewsTests(TestCase):
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

        self.paid_order = Order.objects.create(
            user=self.user,
            full_name="Joe Smith",
            email="joe@example.com",
            phone="123456789",
            address1="Main Street 1",
            city="Stockholm",
            postcode="12345",
            country="Sweden",
            subtotal=Decimal("100.00"),
            tax=Decimal("25.00"),
            total=Decimal("125.00"),
            is_paid=True,
        )

        self.unpaid_order = Order.objects.create(
            user=self.user,
            full_name="Joe Smith",
            email="joe@example.com",
            phone="123456789",
            address1="Main Street 1",
            city="Stockholm",
            postcode="12345",
            country="Sweden",
            subtotal=Decimal("50.00"),
            tax=Decimal("12.50"),
            total=Decimal("62.50"),
            is_paid=False,
        )

        self.other_user_order = Order.objects.create(
            user=self.other_user,
            full_name="Other User",
            email="other@example.com",
            phone="999999999",
            address1="Other Street 2",
            city="Gothenburg",
            postcode="54321",
            country="Sweden",
            subtotal=Decimal("200.00"),
            tax=Decimal("50.00"),
            total=Decimal("250.00"),
            is_paid=True,
        )

        self.list_url = reverse("orders:list")
        self.paid_detail_url = reverse(
            "orders:detail",
            args=[self.paid_order.order_number],
        )
        self.unpaid_detail_url = reverse(
            "orders:detail",
            args=[self.unpaid_order.order_number],
        )

    def test_order_list_requires_login(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_user_can_view_order_list(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "orders/order_list.html",
        )
        self.assertIn("orders", response.context)

    def test_order_list_shows_only_paid_orders_for_current_user(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(self.list_url)
        orders = response.context["orders"]

        self.assertIn(self.paid_order, orders)
        self.assertNotIn(self.unpaid_order, orders)
        self.assertNotIn(self.other_user_order, orders)

    def test_order_detail_requires_login(self):
        response = self.client.get(self.paid_detail_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_user_can_view_paid_order_detail(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(self.paid_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "orders/order_detail.html",
        )
        self.assertEqual(response.context["order"], self.paid_order)

    def test_user_cannot_view_another_users_order_detail(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(
            reverse(
                "orders:detail",
                args=[self.other_user_order.order_number],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_unpaid_order_detail_redirects_to_cart(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(self.unpaid_detail_url)

        self.assertRedirects(response, reverse("cart:detail"))
