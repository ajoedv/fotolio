from django.contrib.admin.sites import site
from django.test import SimpleTestCase

from profiles.admin import ProfileAdmin
from profiles.models import Profile


class ProfileAdminTests(SimpleTestCase):
    def test_profile_is_registered(self):
        self.assertIn(Profile, site._registry)

    def test_profile_uses_correct_admin_class(self):
        self.assertIsInstance(
            site._registry[Profile],
            ProfileAdmin,
        )

    def test_profile_admin_list_display(self):
        admin_obj = site._registry[Profile]

        self.assertEqual(
            admin_obj.list_display,
            ("user", "display_name", "phone"),
        )
