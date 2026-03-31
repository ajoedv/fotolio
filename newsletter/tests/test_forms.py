from django.test import TestCase

from newsletter.forms import NewsletterSubscribeForm


class NewsletterSubscribeFormTests(TestCase):
    def test_form_is_valid_with_valid_email(self):
        form = NewsletterSubscribeForm(
            {"email": "test@example.com"}
        )

        self.assertTrue(form.is_valid())

    def test_form_is_invalid_without_email(self):
        form = NewsletterSubscribeForm({"email": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_is_invalid_with_invalid_email(self):
        form = NewsletterSubscribeForm(
            {"email": "not-an-email"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
