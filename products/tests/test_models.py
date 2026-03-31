from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from products.models import Category, Product, ProductReview


class CategoryModelTests(TestCase):
    def test_str_returns_name(self):
        category = Category.objects.create(
            name="landscape",
            friendly_name="Landscape",
        )

        self.assertEqual(str(category), "landscape")

    def test_get_friendly_name_returns_friendly_name(self):
        category = Category.objects.create(
            name="abstract",
            friendly_name="Abstract Art",
        )

        self.assertEqual(
            category.get_friendly_name(),
            "Abstract Art",
        )

    def test_get_friendly_name_returns_name_when_blank(self):
        category = Category.objects.create(
            name="portrait",
            friendly_name="",
        )

        self.assertEqual(
            category.get_friendly_name(),
            "portrait",
        )


class ProductModelTests(TestCase):
    def test_str_returns_product_name(self):
        product = Product.objects.create(
            name="Sunset Print",
            description="Beautiful sunset wall art.",
            price=Decimal("49.99"),
        )

        self.assertEqual(str(product), "Sunset Print")


class ProductReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password="testpass123",
        )
        self.product = Product.objects.create(
            name="Ocean Print",
            description="Ocean wall art.",
            price=Decimal("59.99"),
        )

    def test_str_returns_expected_format(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Excellent quality.",
        )

        self.assertEqual(
            str(review),
            "Ocean Print - joe (5/5)",
        )

    def test_reviews_are_ordered_by_created_at_desc(self):
        first_user = User.objects.create_user(
            username="firstuser",
            email="first@example.com",
            password="testpass123",
        )
        second_user = User.objects.create_user(
            username="seconduser",
            email="second@example.com",
            password="testpass123",
        )

        older_review = ProductReview.objects.create(
            product=self.product,
            user=first_user,
            rating=4,
            comment="Older review.",
        )
        newer_review = ProductReview.objects.create(
            product=self.product,
            user=second_user,
            rating=5,
            comment="Newer review.",
        )

        reviews = list(ProductReview.objects.all())

        self.assertEqual(reviews[0], newer_review)
        self.assertEqual(reviews[1], older_review)

    def test_product_and_user_combination_must_be_unique(self):
        ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="First review.",
        )

        duplicate_review = ProductReview(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Duplicate review.",
        )

        with self.assertRaises(IntegrityError):
            duplicate_review.save()
