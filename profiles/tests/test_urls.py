from django.test import SimpleTestCase
from django.urls import resolve, reverse

from profiles.views import (
    delete_profile,
    edit_profile,
    profile_view,
)


class ProfileUrlsTests(SimpleTestCase):
    def test_profile_url_resolves(self):
        url = reverse("profiles:profile")

        self.assertEqual(url, "/profile/")
        self.assertEqual(resolve(url).func, profile_view)

    def test_edit_profile_url_resolves(self):
        url = reverse("profiles:edit")

        self.assertEqual(url, "/profile/edit/")
        self.assertEqual(resolve(url).func, edit_profile)

    def test_delete_profile_url_resolves(self):
        url = reverse("profiles:delete")

        self.assertEqual(url, "/profile/delete/")
        self.assertEqual(resolve(url).func, delete_profile)
