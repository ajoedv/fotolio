from django.test import TestCase

from home.forms import ContactMessageForm


class ContactMessageFormTests(TestCase):
    def test_form_is_valid_with_required_fields(self):
        form = ContactMessageForm(
            {
                "name": "Joe",
                "email": "joe@example.com",
                "subject": "Custom print inquiry",
                "message": "I want to ask about print sizes.",
            }
        )

        self.assertTrue(form.is_valid())

    def test_name_is_required(self):
        form = ContactMessageForm(
            {
                "name": "",
                "email": "joe@example.com",
                "subject": "Custom print inquiry",
                "message": "I want to ask about print sizes.",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_email_is_required(self):
        form = ContactMessageForm(
            {
                "name": "Joe",
                "email": "",
                "subject": "Custom print inquiry",
                "message": "I want to ask about print sizes.",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_email_must_be_valid_format(self):
        form = ContactMessageForm(
            {
                "name": "Joe",
                "email": "not-an-email",
                "subject": "Custom print inquiry",
                "message": "I want to ask about print sizes.",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_subject_is_required(self):
        form = ContactMessageForm(
            {
                "name": "Joe",
                "email": "joe@example.com",
                "subject": "",
                "message": "I want to ask about print sizes.",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("subject", form.errors)

    def test_message_is_required(self):
        form = ContactMessageForm(
            {
                "name": "Joe",
                "email": "joe@example.com",
                "subject": "Custom print inquiry",
                "message": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_phone_field_is_not_in_form(self):
        form = ContactMessageForm()

        self.assertNotIn("phone", form.fields)
