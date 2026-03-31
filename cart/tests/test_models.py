from django.contrib.auth.models import User
from django.test import TestCase

from cart.models import CartItem
from products.models import Category, Product


class CartItemModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="joe",
            password="testpass123",
        )
        self.category = Category.objects.create(
            name="prints",
            friendly_name="Prints",
        )
        self.product = Product.objects.create(
            category=self.category,
            sku="TEST123",
            name="Test Product",
            description="Test description",
            price=99.99,
            image_url="https://example.com/image.jpg",
        )

    def test_string_representation_returns_product_name_and_quantity(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(str(cart_item), "Test Product x 2")

    def test_unit_price_returns_product_price(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(cart_item.unit_price, self.product.price)

    def test_line_total_returns_unit_price_multiplied_by_quantity(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=3,
        )

        self.assertEqual(cart_item.line_total, self.product.price * 3)
