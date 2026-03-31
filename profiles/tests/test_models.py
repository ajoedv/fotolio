from django.contrib.auth.models import User
from django.test import TestCase

from profiles.models import Profile


class ProfileModelTests(TestCase):
    def test_profile_is_created_for_user(self):
        user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password="testpass123",
        )

        self.assertTrue(
            Profile.objects.filter(user=user).exists()
        )

        profile = Profile.objects.get(user=user)

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.display_name, "")
        self.assertEqual(profile.phone, "")

    def test_str_returns_display_name_when_present(self):
        user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password="testpass123",
        )
        profile = Profile.objects.get(user=user)
        profile.display_name = "Joe Design"
        profile.save()

        self.assertEqual(str(profile), "Joe Design")

    def test_str_returns_username_when_display_name_is_blank(self):
        user = User.objects.create_user(
            username="joeuser",
            email="joe@example.com",
            password="testpass123",
        )
        profile = Profile.objects.get(user=user)
        profile.display_name = ""
        profile.save()

        self.assertEqual(str(profile), "joeuser")
