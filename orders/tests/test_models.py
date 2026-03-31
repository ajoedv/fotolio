from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from orders.models import Order, OrderLineItem
from products.models import Product


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password="testpass123",
        )

    def test_order_generates_number_year_and_sequence_on_save(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Joe Smith",
            email="joe@example.com",
            phone="123456789",
            address1="Main Street 1",
            city="Stockholm",
            postcode="12345",
            country="Sweden",
        )

        self.assertIsNotNone(order.order_number)
        self.assertIsNotNone(order.order_year)
        self.assertIsNotNone(order.order_seq)
        self.assertTrue(order.order_number.startswith("FO-"))
        self.assertEqual(order.order_seq, 1)

    def test_second_order_in_same_year_gets_next_sequence(self):
        first_order = Order.objects.create(
            user=self.user,
            full_name="Joe Smith",
            email="joe@example.com",
            phone="123456789",
            address1="Main Street 1",
            city="Stockholm",
            postcode="12345",
            country="Sweden",
        )

        second_order = Order.objects.create(
            user=self.user,
            full_name="Joe Smith",
            email="joe@example.com",
            phone="123456789",
            address1="Main Street 1",
            city="Stockholm",
            postcode="12345",
            country="Sweden",
        )

        self.assertEqual(first_order.order_seq, 1)
        self.assertEqual(second_order.order_seq, 2)
        self.assertEqual(
            second_order.order_year,
            first_order.order_year,
        )

    def test_order_str_returns_order_number(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Joe Smith",
            email="joe@example.com",
            phone="123456789",
            address1="Main Street 1",
            city="Stockholm",
            postcode="12345",
            country="Sweden",
        )

        self.assertEqual(
            str(order),
            f"Order {order.order_number}",
        )


class OrderLineItemModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password="testpass123",
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name="Joe Smith",
            email="joe@example.com",
            phone="123456789",
            address1="Main Street 1",
            city="Stockholm",
            postcode="12345",
            country="Sweden",
        )
        self.product = Product.objects.create(
            name="Sunset Print",
            description="Beautiful sunset artwork.",
            price=Decimal("49.99"),
        )

    def test_order_lineitem_str_returns_name_and_quantity(self):
        lineitem = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            product_name="Sunset Print",
            quantity=2,
            line_total=Decimal("99.98"),
        )

        self.assertEqual(str(lineitem), "Sunset Print x 2")
