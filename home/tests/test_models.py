from django.test import TestCase

from home.models import ContactMessage


class ContactMessageModelTests(TestCase):
    def test_string_representation_returns_subject_and_email(self):
        message = ContactMessage.objects.create(
            name="Joe",
            email="joe@example.com",
            subject="Custom print inquiry",
            message="I want to ask about print sizes.",
        )

        self.assertEqual(
            str(message),
            "Custom print inquiry - joe@example.com",
        )

    def test_default_ordering_is_newest_first(self):
        older_message = ContactMessage.objects.create(
            name="Joe",
            email="joe1@example.com",
            subject="First subject",
            message="First message",
        )
        newer_message = ContactMessage.objects.create(
            name="Joe",
            email="joe2@example.com",
            subject="Second subject",
            message="Second message",
        )

        messages = list(ContactMessage.objects.all())

        self.assertEqual(messages[0], newer_message)
        self.assertEqual(messages[1], older_message)
