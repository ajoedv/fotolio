from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from home.models import ContactMessage
from products.models import Category, Product


class HomeViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="prints",
            friendly_name="Prints",
        )
        self.product = Product.objects.create(
            category=self.category,
            sku="TEST123",
            name="Test Product",
            description="Test description",
            price=99.99,
            image_url="https://example.com/image.jpg",
        )

    def test_index_view_returns_200_and_uses_correct_template(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertIn("teaser_products", response.context)

    def test_about_view_returns_200_and_uses_correct_template(self):
        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/about.html")
        self.assertIn("teaser_products", response.context)

    def test_contact_view_get_returns_200_and_uses_correct_template(self):
        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/contact.html")
        self.assertIn("form", response.context)
        self.assertIn("teaser_products", response.context)

    def test_contact_view_post_valid_data_creates_message(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Joe",
                "email": "joe@example.com",
                "subject": "Custom print inquiry",
                "message": "I want to ask about print sizes.",
            },
            follow=True,
        )

        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertRedirects(response, reverse("contact"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Message sent successfully.",
        )

    def test_contact_view_post_invalid_data_does_not_create_message(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "",
                "email": "joe@example.com",
                "subject": "Custom print inquiry",
                "message": "I want to ask about print sizes.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/contact.html")
        self.assertEqual(ContactMessage.objects.count(), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Please correct the errors below.",
        )
