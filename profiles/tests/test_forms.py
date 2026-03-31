from django.test import TestCase

from profiles.forms import ProfileForm


class ProfileFormTests(TestCase):
    def test_required_fields_are_required(self):
        form = ProfileForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn("display_name", form.errors)
        self.assertIn("phone", form.errors)
        self.assertIn("shipping_full_name", form.errors)
        self.assertIn("address_line1", form.errors)
        self.assertIn("city", form.errors)
        self.assertIn("postcode", form.errors)
        self.assertIn("country", form.errors)

    def test_address_line2_is_not_required(self):
        form = ProfileForm(
            data={
                "display_name": "Joe",
                "phone": "123456789",
                "shipping_full_name": "Joe Smith",
                "address_line1": "Main Street 1",
                "city": "Stockholm",
                "postcode": "12345",
                "country": "SE",
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_is_valid_with_complete_required_data(self):
        form = ProfileForm(
            data={
                "display_name": "Joe",
                "phone": "123456789",
                "shipping_full_name": "Joe Smith",
                "address_line1": "Main Street 1",
                "address_line2": "Apartment 2",
                "city": "Stockholm",
                "postcode": "12345",
                "country": "SE",
            }
        )

        self.assertTrue(form.is_valid())

    def test_display_name_field_has_expected_placeholder(self):
        form = ProfileForm()

        self.assertEqual(
            form.fields["display_name"].widget.attrs["placeholder"],
            "Display name",
        )

    def test_country_field_has_form_control_class(self):
        form = ProfileForm()

        self.assertEqual(
            form.fields["country"].widget.attrs["class"],
            "form-control",
        )
