from django.test import SimpleTestCase
from django.urls import resolve, reverse

from products.views import (
    ping,
    product_detail,
    products_list,
    review_create,
    review_delete,
    review_edit,
)


class ProductUrlsTests(SimpleTestCase):
    def test_ping_url_resolves(self):
        url = reverse("products:ping")

        self.assertEqual(url, "/products/ping/")
        self.assertEqual(resolve(url).func, ping)

    def test_products_list_url_resolves(self):
        url = reverse("products:list")

        self.assertEqual(url, "/products/")
        self.assertEqual(resolve(url).func, products_list)

    def test_product_detail_url_resolves(self):
        url = reverse("products:detail", args=[1])

        self.assertEqual(url, "/products/1/")
        self.assertEqual(resolve(url).func, product_detail)

    def test_review_add_url_resolves(self):
        url = reverse("products:review_add", args=[1])

        self.assertEqual(url, "/products/1/reviews/add/")
        self.assertEqual(resolve(url).func, review_create)

    def test_review_edit_url_resolves(self):
        url = reverse("products:review_edit", args=[1])

        self.assertEqual(url, "/products/reviews/1/edit/")
        self.assertEqual(resolve(url).func, review_edit)

    def test_review_delete_url_resolves(self):
        url = reverse("products:review_delete", args=[1])

        self.assertEqual(url, "/products/reviews/1/delete/")
        self.assertEqual(resolve(url).func, review_delete)
