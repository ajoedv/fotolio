from django.test import SimpleTestCase
from django.urls import resolve, reverse

from orders.views import order_detail, order_list


class OrderUrlsTests(SimpleTestCase):
    def test_order_list_url_resolves(self):
        url = reverse("orders:list")

        self.assertEqual(url, "/orders/")
        self.assertEqual(resolve(url).func, order_list)

    def test_order_detail_url_resolves(self):
        url = reverse("orders:detail", args=["FO-2026-000001"])

        self.assertEqual(url, "/orders/FO-2026-000001/")
        self.assertEqual(resolve(url).func, order_detail)
