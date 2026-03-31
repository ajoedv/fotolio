from decimal import Decimal

from django.test import RequestFactory, TestCase, override_settings

from fotolio.urls import custom_server_error
from products.models import Product


@override_settings(ALLOWED_HOSTS=["testserver", "localhost"])
class ProjectViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_robots_txt_returns_success(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertTemplateUsed(response, "robots.txt")

    def test_sitemap_xml_returns_success(self):
        Product.objects.create(
            name="Sunset Print",
            description="Beautiful sunset artwork.",
            price=Decimal("49.99"),
        )

        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<urlset", status_code=200)
        self.assertContains(response, "/products/1/", status_code=200)

    @override_settings(DEBUG=False)
    def test_custom_404_page_is_used(self):
        response = self.client.get("/this-page-does-not-exist/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    @override_settings(DEBUG=False)
    def test_custom_500_page_is_used(self):
        request = self.factory.get("/test-500/")
        response = custom_server_error(request)

        self.assertEqual(response.status_code, 500)
