from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product, ProductReview


class ProductViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )

        self.category = Category.objects.create(
            name="landscape",
            friendly_name="Landscape",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Sunset Print",
            description="Beautiful sunset artwork.",
            price=Decimal("49.99"),
        )

        self.second_product = Product.objects.create(
            category=self.category,
            name="Ocean Print",
            description="Ocean wall art.",
            price=Decimal("59.99"),
        )

        self.list_url = reverse("products:list")
        self.detail_url = reverse(
            "products:detail",
            args=[self.product.pk],
        )
        self.review_add_url = reverse(
            "products:review_add",
            args=[self.product.pk],
        )

    def test_ping_view_returns_ok_response(self):
        response = self.client.get(reverse("products:ping"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Products route OK")

    def test_products_list_view_returns_success(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/list.html")
        self.assertIn("products", response.context)
        self.assertIn("categories", response.context)

    def test_products_list_filters_by_category(self):
        other_category = Category.objects.create(
            name="abstract",
            friendly_name="Abstract",
        )
        Product.objects.create(
            category=other_category,
            name="Abstract Print",
            description="Abstract wall art.",
            price=Decimal("39.99"),
        )

        response = self.client.get(
            self.list_url,
            {"category": "landscape"},
        )

        products = response.context["products"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(products.count(), 2)
        self.assertEqual(response.context["active_category"], "landscape")

    def test_products_list_with_invalid_category_returns_no_products(self):
        response = self.client.get(
            self.list_url,
            {"category": "invalid-category"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"].count(), 0)
        self.assertTrue(response.context["no_results"])

    def test_products_list_search_returns_matching_products(self):
        response = self.client.get(
            self.list_url,
            {"q": "sunset"},
        )

        products = response.context["products"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first(), self.product)
        self.assertEqual(response.context["search_query"], "sunset")

    def test_products_list_search_with_no_results_sets_no_results_true(self):
        response = self.client.get(
            self.list_url,
            {"q": "notfoundterm"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"].count(), 0)
        self.assertTrue(response.context["no_results"])

    def test_products_list_sets_show_search_when_focus_is_one(self):
        response = self.client.get(
            self.list_url,
            {"focus": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["show_search"])
        self.assertTrue(response.context["autofocus_search"])

    def test_product_detail_view_returns_success(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/detail.html")
        self.assertEqual(response.context["product"], self.product)
        self.assertIn("reviews", response.context)
        self.assertIn("teaser_products", response.context)

    def test_product_detail_view_returns_404_for_invalid_product(self):
        response = self.client.get(
            reverse("products:detail", args=[9999])
        )

        self.assertEqual(response.status_code, 404)

    def test_product_detail_sets_user_review_for_authenticated_user(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Excellent.",
        )

        self.client.login(
            username="joe",
            password="testpass123",
        )
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user_review"], review)

    def test_review_add_requires_login(self):
        response = self.client.get(self.review_add_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_review_add_get_returns_form_for_logged_in_user(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(self.review_add_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "products/reviews/review_form.html",
        )
        self.assertEqual(response.context["product"], self.product)
        self.assertEqual(response.context["mode"], "create")
        self.assertIn("form", response.context)

    def test_review_add_post_creates_review(self):
        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.post(
            self.review_add_url,
            {
                "rating": 5,
                "comment": "Amazing print.",
            },
        )

        self.assertRedirects(
            response,
            reverse("products:detail", args=[self.product.pk]),
        )
        self.assertTrue(
            ProductReview.objects.filter(
                product=self.product,
                user=self.user,
            ).exists()
        )

    def test_review_add_redirects_to_edit_if_review_already_exists(self):
        existing_review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Already reviewed.",
        )

        self.client.login(
            username="joe",
            password="testpass123",
        )

        response = self.client.get(self.review_add_url)

        self.assertRedirects(
            response,
            reverse(
                "products:review_edit",
                args=[existing_review.pk],
            ),
        )

    def test_review_edit_allows_owner_to_view_form(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Initial review.",
        )

        self.client.login(
            username="joe",
            password="testpass123",
        )
        response = self.client.get(
            reverse("products:review_edit", args=[review.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "products/reviews/review_form.html",
        )
        self.assertEqual(response.context["mode"], "edit")

    def test_review_edit_rejects_non_owner(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Initial review.",
        )

        self.client.login(
            username="otheruser",
            password="testpass123",
        )
        response = self.client.get(
            reverse("products:review_edit", args=[review.pk])
        )

        self.assertRedirects(
            response,
            reverse("products:detail", args=[self.product.pk]),
        )

    def test_review_edit_post_updates_review_for_owner(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Initial review.",
        )

        self.client.login(
            username="joe",
            password="testpass123",
        )
        response = self.client.post(
            reverse("products:review_edit", args=[review.pk]),
            {
                "rating": 5,
                "comment": "Updated review.",
            },
        )

        self.assertRedirects(
            response,
            reverse("products:detail", args=[self.product.pk]),
        )

        review.refresh_from_db()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Updated review.")

    def test_review_delete_requires_login(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Delete me.",
        )

        response = self.client.post(
            reverse("products:review_delete", args=[review.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_review_delete_rejects_non_owner(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Delete me.",
        )

        self.client.login(
            username="otheruser",
            password="testpass123",
        )
        response = self.client.post(
            reverse("products:review_delete", args=[review.pk])
        )

        self.assertRedirects(
            response,
            reverse("products:detail", args=[self.product.pk]),
        )
        self.assertTrue(
            ProductReview.objects.filter(pk=review.pk).exists()
        )

    def test_review_delete_get_does_not_delete_review(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Delete me.",
        )

        self.client.login(
            username="joe",
            password="testpass123",
        )
        response = self.client.get(
            reverse("products:review_delete", args=[review.pk])
        )

        self.assertRedirects(
            response,
            reverse("products:detail", args=[self.product.pk]),
        )
        self.assertTrue(
            ProductReview.objects.filter(pk=review.pk).exists()
        )

    def test_review_delete_post_deletes_review_for_owner(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Delete me.",
        )

        self.client.login(
            username="joe",
            password="testpass123",
        )
        response = self.client.post(
            reverse("products:review_delete", args=[review.pk])
        )

        self.assertRedirects(
            response,
            reverse("products:detail", args=[self.product.pk]),
        )
        self.assertFalse(
            ProductReview.objects.filter(pk=review.pk).exists()
        )
