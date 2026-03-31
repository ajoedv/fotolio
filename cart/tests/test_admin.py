from django.contrib.admin.sites import site
from django.test import SimpleTestCase

from cart.admin import CartItemAdmin
from cart.models import CartItem


class CartAdminTests(SimpleTestCase):
    def test_cart_item_is_registered(self):
        self.assertIn(CartItem, site._registry)

    def test_cart_item_uses_correct_admin_class(self):
        self.assertIsInstance(
            site._registry[CartItem],
            CartItemAdmin,
        )

    def test_cart_item_admin_list_display(self):
        admin_obj = site._registry[CartItem]

        self.assertEqual(
            admin_obj.list_display,
            ("user", "product", "quantity"),
        )

    def test_cart_item_admin_list_filter(self):
        admin_obj = site._registry[CartItem]

        self.assertEqual(
            admin_obj.list_filter,
            ("user",),
        )
