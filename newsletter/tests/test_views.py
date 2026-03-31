from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from newsletter.models import NewsletterSubscriber


class NewsletterSubscribeViewTests(TestCase):
    def setUp(self):
        self.url = reverse("newsletter:subscribe")

    def test_get_request_is_not_allowed(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)

    def test_valid_post_creates_new_subscriber(self):
        response = self.client.post(
            self.url,
            {"email": "test@example.com"},
            HTTP_REFERER="/contact/",
            follow=True,
        )

        self.assertEqual(
            NewsletterSubscriber.objects.count(),
            1,
        )
        self.assertTrue(
            NewsletterSubscriber.objects.filter(
                email="test@example.com"
            ).exists()
        )
        self.assertRedirects(response, "/contact/")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Subscribed! Welcome to Fotolio updates.",
        )

    def test_valid_post_with_existing_email_does_not_create_duplicate(self):
        NewsletterSubscriber.objects.create(email="test@example.com")

        response = self.client.post(
            self.url,
            {"email": "test@example.com"},
            HTTP_REFERER="/contact/",
            follow=True,
        )

        self.assertEqual(
            NewsletterSubscriber.objects.count(),
            1,
        )
        self.assertRedirects(response, "/contact/")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "You're already subscribed.",
        )

    def test_invalid_post_does_not_create_subscriber(self):
        response = self.client.post(
            self.url,
            {"email": "not-an-email"},
            HTTP_REFERER="/contact/",
            follow=True,
        )

        self.assertEqual(
            NewsletterSubscriber.objects.count(),
            0,
        )
        self.assertRedirects(response, "/contact/")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Please enter a valid email.",
        )

    def test_post_without_http_referer_redirects_to_home(self):
        response = self.client.post(
            self.url,
            {"email": "test@example.com"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_email_is_saved_lowercased_and_trimmed(self):
        self.client.post(
            self.url,
            {"email": "  TEST@EXAMPLE.COM  "},
            HTTP_REFERER="/",
        )

        self.assertTrue(
            NewsletterSubscriber.objects.filter(
                email="test@example.com"
            ).exists()
        )
