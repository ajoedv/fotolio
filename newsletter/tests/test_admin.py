from django.contrib.admin.sites import site
from django.test import SimpleTestCase

from newsletter.admin import NewsletterSubscriberAdmin
from newsletter.models import NewsletterSubscriber


class NewsletterAdminTests(SimpleTestCase):
    def test_newsletter_subscriber_is_registered(self):
        self.assertIn(NewsletterSubscriber, site._registry)

    def test_newsletter_subscriber_uses_correct_admin_class(self):
        self.assertIsInstance(
            site._registry[NewsletterSubscriber],
            NewsletterSubscriberAdmin,
        )

    def test_newsletter_admin_list_display(self):
        admin_obj = site._registry[NewsletterSubscriber]

        self.assertEqual(
            admin_obj.list_display,
            ("email", "created_at"),
        )

    def test_newsletter_admin_search_fields(self):
        admin_obj = site._registry[NewsletterSubscriber]

        self.assertEqual(
            admin_obj.search_fields,
            ("email",),
        )
