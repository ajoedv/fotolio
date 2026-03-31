from django.contrib.admin.sites import site
from django.test import SimpleTestCase

from home.admin import ContactMessageAdmin
from home.models import ContactMessage


class HomeAdminTests(SimpleTestCase):
    def test_contact_message_is_registered(self):
        self.assertIn(ContactMessage, site._registry)

    def test_contact_message_uses_correct_admin_class(self):
        self.assertIsInstance(
            site._registry[ContactMessage],
            ContactMessageAdmin,
        )

    def test_contact_message_admin_list_display(self):
        admin_obj = site._registry[ContactMessage]

        self.assertEqual(
            admin_obj.list_display,
            ("created_at", "subject", "email", "is_read"),
        )

    def test_contact_message_admin_list_filter(self):
        admin_obj = site._registry[ContactMessage]

        self.assertEqual(
            admin_obj.list_filter,
            ("is_read", "created_at"),
        )

    def test_contact_message_admin_search_fields(self):
        admin_obj = site._registry[ContactMessage]

        self.assertEqual(
            admin_obj.search_fields,
            ("name", "email", "subject", "message"),
        )

    def test_contact_message_admin_ordering(self):
        admin_obj = site._registry[ContactMessage]

        self.assertEqual(
            admin_obj.ordering,
            ("-created_at",),
        )
