from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from profiles.models import Profile


class ProfileViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password="testpass123",
        )
        self.profile_url = reverse("profiles:profile")
        self.edit_url = reverse("profiles:edit")
        self.delete_url = reverse("profiles:delete")

    def test_profile_view_requires_login(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_user_can_view_profile_page(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "profiles/profile.html",
        )
        self.assertIn("profile", response.context)

    def test_profile_view_creates_profile_if_missing(self):
        Profile.objects.filter(user=self.user).delete()
        self.assertFalse(
            Profile.objects.filter(user=self.user).exists()
        )

        self.client.login(
            username="joe",
            password="testpass123",
        )
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Profile.objects.filter(user=self.user).exists()
        )

    def test_edit_profile_requires_login(self):
        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_user_can_view_edit_profile_page(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "profiles/edit.html",
        )
        self.assertIn("form", response.context)
        self.assertIn("profile", response.context)

    def test_edit_profile_post_updates_profile(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        session = self.client.session
        session["checkout_shipping"] = {
            "city": "Old City",
        }
        session.save()

        response = self.client.post(
            self.edit_url,
            {
                "display_name": "Joe Design",
                "phone": "123456789",
                "shipping_full_name": "Joe Smith",
                "address_line1": "Main Street 1",
                "address_line2": "Apartment 2",
                "city": "Stockholm",
                "postcode": "12345",
                "country": "SE",
            },
        )

        self.assertRedirects(
            response,
            reverse("profiles:profile"),
        )

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.display_name, "Joe Design")
        self.assertEqual(profile.city, "Stockholm")

        session = self.client.session
        self.assertNotIn("checkout_shipping", session)

    def test_edit_profile_post_with_invalid_data_returns_form(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.post(
            self.edit_url,
            {
                "display_name": "",
                "phone": "",
                "shipping_full_name": "",
                "address_line1": "",
                "city": "",
                "postcode": "",
                "country": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "profiles/edit.html",
        )
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)

    def test_delete_profile_requires_login(self):
        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_profile_get_shows_confirmation_page(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "profiles/delete_confirm.html",
        )

    def test_delete_profile_post_deletes_user_and_redirects_home(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.post(self.delete_url)

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(
            User.objects.filter(username="joe").exists()
        )
