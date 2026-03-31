from django.test import TestCase

from products.forms import ProductReviewForm


class ProductReviewFormTests(TestCase):
    def test_form_is_valid_with_valid_data(self):
        form = ProductReviewForm(
            data={
                "rating": 5,
                "comment": "Excellent product.",
            }
        )

        self.assertTrue(form.is_valid())

    def test_rating_is_required(self):
        form = ProductReviewForm(
            data={
                "comment": "Excellent product.",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_comment_is_required(self):
        form = ProductReviewForm(
            data={
                "rating": 5,
                "comment": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("comment", form.errors)

    def test_rating_must_not_be_less_than_one(self):
        form = ProductReviewForm(
            data={
                "rating": 0,
                "comment": "Too low rating value.",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_rating_must_not_be_greater_than_five(self):
        form = ProductReviewForm(
            data={
                "rating": 6,
                "comment": "Too high rating value.",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_rating_field_uses_hidden_input(self):
        form = ProductReviewForm()

        self.assertEqual(
            form.fields["rating"].widget.__class__.__name__,
            "HiddenInput",
        )

    def test_comment_field_has_expected_placeholder(self):
        form = ProductReviewForm()

        self.assertEqual(
            form.fields["comment"].widget.attrs["placeholder"],
            "Write your review...",
        )

    def test_comment_field_has_expected_rows(self):
        form = ProductReviewForm()

        self.assertEqual(
            form.fields["comment"].widget.attrs["rows"],
            4,
        )
