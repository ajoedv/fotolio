from django.test import SimpleTestCase
from django.urls import resolve, reverse

from cart.views import (
    add_to_cart,
    checkout,
    detail,
    payment,
    remove_item,
    success,
    update_item,
)


class CartUrlsTests(SimpleTestCase):
    def test_detail_url_resolves(self):
        url = reverse("cart:detail")
        resolved = resolve(url)

        self.assertEqual(resolved.func, detail)

    def test_checkout_url_resolves(self):
        url = reverse("cart:checkout")
        resolved = resolve(url)

        self.assertEqual(resolved.func, checkout)

    def test_payment_url_resolves(self):
        url = reverse("cart:payment")
        resolved = resolve(url)

        self.assertEqual(resolved.func, payment)

    def test_success_url_resolves(self):
        url = reverse("cart:success")
        resolved = resolve(url)

        self.assertEqual(resolved.func, success)

    def test_add_to_cart_url_resolves(self):
        url = reverse("cart:add", args=[1])
        resolved = resolve(url)

        self.assertEqual(resolved.func, add_to_cart)

    def test_update_item_url_resolves(self):
        url = reverse("cart:update", args=[1])
        resolved = resolve(url)

        self.assertEqual(resolved.func, update_item)

    def test_remove_item_url_resolves(self):
        url = reverse("cart:remove", args=[1])
        resolved = resolve(url)

        self.assertEqual(resolved.func, remove_item)
