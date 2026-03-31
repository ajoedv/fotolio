from django.db import IntegrityError
from django.test import TestCase

from newsletter.models import NewsletterSubscriber


class NewsletterSubscriberModelTests(TestCase):
    def test_string_representation_returns_email(self):
        subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com"
        )

        self.assertEqual(str(subscriber), "test@example.com")

    def test_email_must_be_unique(self):
        NewsletterSubscriber.objects.create(email="test@example.com")

        with self.assertRaises(IntegrityError):
            NewsletterSubscriber.objects.create(email="test@example.com")
