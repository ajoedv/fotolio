from django.contrib.auth.models import User
from django.test import TestCase

from profiles.models import Profile


class ProfileSignalTests(TestCase):
    def test_profile_is_created_when_user_is_created(self):
        user = User.objects.create_user(
            username="signaluser",
            email="signal@example.com",
            password="testpass123",
        )

        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_missing_profile_is_created_when_existing_user_is_saved(self):
        user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="testpass123",
        )

        Profile.objects.filter(user=user).delete()
        self.assertFalse(Profile.objects.filter(user=user).exists())

        user.first_name = "Joe"
        user.save()

        self.assertTrue(Profile.objects.filter(user=user).exists())
