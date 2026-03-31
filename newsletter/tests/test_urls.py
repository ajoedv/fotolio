from django.test import SimpleTestCase
from django.urls import resolve, reverse

from newsletter.views import subscribe


class NewsletterUrlsTests(SimpleTestCase):
    def test_subscribe_url_resolves(self):
        url = reverse("newsletter:subscribe")
        resolved = resolve(url)

        self.assertEqual(resolved.func, subscribe)
