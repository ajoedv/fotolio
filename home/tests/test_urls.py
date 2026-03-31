from django.test import SimpleTestCase
from django.urls import resolve, reverse

from home.views import about, contact, index


class HomeUrlsTests(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse("home")
        resolved = resolve(url)

        self.assertEqual(resolved.func, index)

    def test_about_url_resolves(self):
        url = reverse("about")
        resolved = resolve(url)

        self.assertEqual(resolved.func, about)

    def test_contact_url_resolves(self):
        url = reverse("contact")
        resolved = resolve(url)

        self.assertEqual(resolved.func, contact)
