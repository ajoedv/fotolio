from django.contrib.admin.sites import site
from django.test import SimpleTestCase

from products.admin import CategoryAdmin, ProductAdmin
from products.models import Category, Product


class ProductAdminTests(SimpleTestCase):
    def test_category_is_registered(self):
        self.assertIn(Category, site._registry)

    def test_category_uses_correct_admin_class(self):
        self.assertIsInstance(
            site._registry[Category],
            CategoryAdmin,
        )

    def test_category_admin_list_display(self):
        admin_obj = site._registry[Category]

        self.assertEqual(
            admin_obj.list_display,
            ("name", "friendly_name"),
        )

    def test_category_admin_search_fields(self):
        admin_obj = site._registry[Category]

        self.assertEqual(
            admin_obj.search_fields,
            ("name", "friendly_name"),
        )

    def test_product_is_registered(self):
        self.assertIn(Product, site._registry)

    def test_product_uses_correct_admin_class(self):
        self.assertIsInstance(
            site._registry[Product],
            ProductAdmin,
        )

    def test_product_admin_list_display(self):
        admin_obj = site._registry[Product]

        self.assertEqual(
            admin_obj.list_display,
            ("name", "category", "price", "sku"),
        )

    def test_product_admin_list_filter(self):
        admin_obj = site._registry[Product]

        self.assertEqual(
            admin_obj.list_filter,
            ("category",),
        )

    def test_product_admin_search_fields(self):
        admin_obj = site._registry[Product]

        self.assertEqual(
            admin_obj.search_fields,
            ("name", "description", "sku"),
        )
