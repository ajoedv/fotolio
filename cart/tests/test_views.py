from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, override_settings
from django.urls import reverse

from cart.models import CartItem
from orders.models import Order
from products.models import Category, Product
from profiles.models import Profile


@override_settings(
    STRIPE_SECRET_KEY="sk_test_dummy",
    STRIPE_PUBLIC_KEY="pk_test_dummy",
    STRIPE_CURRENCY="sek",
)
class CartViewsTests(TestCase):
    def setUp(self):
        self.password = "testpass123"
        self.user = User.objects.create_user(
            username="joe",
            email="joe@example.com",
            password=self.password,
        )
        self.category = Category.objects.create(
            name="prints",
            friendly_name="Prints",
        )
        self.product = Product.objects.create(
            category=self.category,
            sku="TEST123",
            name="Test Product",
            description="Test description",
            price=Decimal("99.99"),
            image_url="https://example.com/image.jpg",
        )

    def login(self):
        self.client.login(
            username="joe",
            password=self.password,
        )

    def create_cart_item(self, quantity=1):
        return CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=quantity,
        )

    def set_checkout_shipping_session(self):
        session = self.client.session
        session["checkout_shipping"] = {
            "full_name": "Joe Example",
            "email": "joe@example.com",
            "phone": "0701234567",
            "address1": "Test Street 1",
            "address2": "",
            "city": "Stockholm",
            "postcode": "11122",
            "country": "SE",
        }
        session.save()

    def checkout_post_data(
        self,
        full_name="Joe Example",
        phone="0701234567",
        address1="Test Street 1",
        address2="",
        city="Stockholm",
        postcode="11122",
        country="SE",
        confirm_details=True,
        save_to_profile=False,
    ):
        data = {
            "full_name": full_name,
            "phone": phone,
            "address1": address1,
            "address2": address2,
            "city": city,
            "postcode": postcode,
            "country": country,
        }

        if confirm_details:
            data["confirm_details"] = "on"

        if save_to_profile:
            data["save_to_profile"] = "on"

        return data

    def test_detail_requires_login(self):
        response = self.client.get(reverse("cart:detail"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_detail_view_returns_200_for_logged_in_user(self):
        self.login()

        response = self.client.get(reverse("cart:detail"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/detail.html")
        self.assertIn("items", response.context)
        self.assertIn("cart_subtotal", response.context)
        self.assertIn("cart_tax", response.context)
        self.assertIn("cart_total", response.context)
        self.assertIn("base_size", response.context)

    def test_add_to_cart_requires_post(self):
        self.login()

        response = self.client.get(
            reverse("cart:add", args=[self.product.id])
        )

        self.assertEqual(response.status_code, 405)

    def test_add_to_cart_creates_new_item(self):
        self.login()

        response = self.client.post(
            reverse("cart:add", args=[self.product.id]),
            {"quantity": 2},
            follow=True,
        )

        self.assertEqual(CartItem.objects.count(), 1)

        item = CartItem.objects.get(
            user=self.user,
            product=self.product,
        )
        self.assertEqual(item.quantity, 2)
        self.assertRedirects(response, reverse("cart:detail"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Added 2 × “Test Product” to your cart.',
        )

    def test_add_to_cart_increases_existing_item_quantity(self):
        self.create_cart_item(quantity=1)
        self.login()

        response = self.client.post(
            reverse("cart:add", args=[self.product.id]),
            {"quantity": 2},
            follow=True,
        )

        self.assertEqual(CartItem.objects.count(), 1)

        item = CartItem.objects.get(
            user=self.user,
            product=self.product,
        )
        self.assertEqual(item.quantity, 3)
        self.assertRedirects(response, reverse("cart:detail"))

    def test_update_item_requires_post(self):
        item = self.create_cart_item(quantity=1)
        self.login()

        response = self.client.get(
            reverse("cart:update", args=[item.id])
        )

        self.assertEqual(response.status_code, 405)

    def test_update_item_changes_quantity(self):
        item = self.create_cart_item(quantity=1)
        self.login()

        response = self.client.post(
            reverse("cart:update", args=[item.id]),
            {"quantity": 4},
            follow=True,
        )

        item.refresh_from_db()
        self.assertEqual(item.quantity, 4)
        self.assertRedirects(response, reverse("cart:detail"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Quantity updated.")

    def test_update_item_never_sets_quantity_below_one(self):
        item = self.create_cart_item(quantity=2)
        self.login()

        self.client.post(
            reverse("cart:update", args=[item.id]),
            {"quantity": 0},
        )

        item.refresh_from_db()
        self.assertEqual(item.quantity, 1)

    def test_remove_item_requires_post(self):
        item = self.create_cart_item(quantity=1)
        self.login()

        response = self.client.get(
            reverse("cart:remove", args=[item.id])
        )

        self.assertEqual(response.status_code, 405)

    def test_remove_item_deletes_item(self):
        item = self.create_cart_item(quantity=1)
        self.login()

        response = self.client.post(
            reverse("cart:remove", args=[item.id]),
            follow=True,
        )

        self.assertEqual(CartItem.objects.count(), 0)
        self.assertRedirects(response, reverse("cart:detail"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Item removed from cart.")

    def test_checkout_redirects_to_detail_when_cart_is_empty(self):
        self.login()

        response = self.client.get(
            reverse("cart:checkout"),
            follow=True,
        )

        self.assertRedirects(response, reverse("cart:detail"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your cart is empty.")

    def test_checkout_get_returns_200_when_cart_has_items(self):
        self.create_cart_item(quantity=2)
        self.login()

        response = self.client.get(reverse("cart:checkout"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/checkout.html")
        self.assertIn("form_data", response.context)
        self.assertIn("errors", response.context)
        self.assertIn("country_choices", response.context)
        self.assertIn("show_shipping_alert", response.context)

    def test_checkout_post_invalid_data_shows_errors(self):
        self.create_cart_item(quantity=1)
        self.login()

        response = self.client.post(
            reverse("cart:checkout"),
            {
                "full_name": "",
                "phone": "",
                "address1": "",
                "address2": "",
                "city": "",
                "postcode": "",
                "country": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/checkout.html")
        self.assertTrue(response.context["errors"])
        self.assertIn("confirm_details", response.context["errors"])

    def test_checkout_post_valid_data_saves_shipping_in_session(self):
        self.create_cart_item(quantity=1)
        self.login()

        response = self.client.post(
            reverse("cart:checkout"),
            self.checkout_post_data(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cart:payment"))

        session = self.client.session
        self.assertIn("checkout_shipping", session)
        self.assertEqual(
            session["checkout_shipping"]["full_name"],
            "Joe Example",
        )
        self.assertEqual(
            session["checkout_shipping"]["country"],
            "SE",
        )

    def test_checkout_post_valid_data_can_save_to_profile(self):
        self.create_cart_item(quantity=1)
        self.login()

        Profile.objects.get_or_create(user=self.user)

        response = self.client.post(
            reverse("cart:checkout"),
            self.checkout_post_data(save_to_profile=True),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cart:payment"))

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.phone, "0701234567")
        self.assertEqual(profile.shipping_full_name, "Joe Example")
        self.assertEqual(profile.address_line1, "Test Street 1")
        self.assertEqual(profile.city, "Stockholm")
        self.assertEqual(profile.postcode, "11122")
        self.assertEqual(str(profile.country), "SE")

    def test_payment_redirects_to_detail_when_cart_is_empty(self):
        self.login()

        response = self.client.get(
            reverse("cart:payment"),
            follow=True,
        )

        self.assertRedirects(response, reverse("cart:detail"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your cart is empty.")

    def test_payment_redirects_to_checkout_when_shipping_missing(self):
        self.create_cart_item(quantity=1)
        self.login()

        response = self.client.get(
            reverse("cart:payment"),
            follow=True,
        )

        self.assertRedirects(response, reverse("cart:checkout"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Please complete checkout before payment.",
        )

    @patch("cart.views.stripe.PaymentIntent.create")
    def test_payment_creates_order_and_renders_payment_page(
        self,
        mock_create,
    ):
        mock_create.return_value = SimpleNamespace(
            id="pi_test_123",
            client_secret="pi_test_123_secret_abc",
        )

        self.create_cart_item(quantity=2)
        self.login()
        self.set_checkout_shipping_session()

        response = self.client.get(reverse("cart:payment"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/payment.html")
        self.assertIn("client_secret", response.context)
        self.assertIn("stripe_public_key", response.context)

        order = Order.objects.get(user=self.user, is_paid=False)
        self.assertEqual(order.email, "joe@example.com")
        self.assertEqual(order.phone, "0701234567")
        self.assertEqual(order.stripe_payment_intent_id, "pi_test_123")

        session = self.client.session
        self.assertEqual(
            session["expected_payment_intent_id"],
            "pi_test_123",
        )
        self.assertIn("pending_order_id", session)

        mock_create.assert_called_once()

    @patch("cart.views.stripe.PaymentIntent.create")
    def test_payment_reuses_existing_pending_order(
        self,
        mock_create,
    ):
        mock_create.return_value = SimpleNamespace(
            id="pi_test_456",
            client_secret="pi_test_456_secret_abc",
        )

        self.create_cart_item(quantity=1)
        self.login()
        self.set_checkout_shipping_session()

        first_response = self.client.get(reverse("cart:payment"))
        self.assertEqual(first_response.status_code, 200)

        first_order = Order.objects.get(user=self.user, is_paid=False)
        order_count_before = Order.objects.count()

        second_response = self.client.get(reverse("cart:payment"))
        self.assertEqual(second_response.status_code, 200)

        self.assertEqual(Order.objects.count(), order_count_before)
        same_order = Order.objects.get(user=self.user, is_paid=False)
        self.assertEqual(first_order.id, same_order.id)

    @patch("cart.views.stripe.PaymentIntent.create")
    def test_payment_redirects_to_checkout_on_stripe_error(
        self,
        mock_create,
    ):
        mock_create.side_effect = Exception("Stripe failure")

        self.create_cart_item(quantity=1)
        self.login()
        self.set_checkout_shipping_session()

        response = self.client.get(
            reverse("cart:payment"),
            follow=True,
        )

        self.assertRedirects(response, reverse("cart:checkout"))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                str(message) == "Stripe error. Please try again."
                for message in messages
            )
        )

    @override_settings(
        STRIPE_SECRET_KEY="",
        STRIPE_PUBLIC_KEY="",
        STRIPE_CURRENCY="sek",
    )
    def test_payment_redirects_to_checkout_when_stripe_keys_missing(self):
        self.create_cart_item(quantity=1)
        self.login()
        self.set_checkout_shipping_session()

        response = self.client.get(
            reverse("cart:payment"),
            follow=True,
        )

        self.assertRedirects(response, reverse("cart:checkout"))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                str(message)
                == "Stripe keys are missing. Please check your settings."
                for message in messages
            )
        )

    def test_success_redirects_to_orders_list_without_payment_intent(self):
        self.login()

        response = self.client.get(reverse("cart:success"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("orders:list"))

    @patch("cart.views.stripe.PaymentIntent.retrieve")
    def test_success_marks_order_paid_and_clears_cart(
        self,
        mock_retrieve,
    ):
        mock_retrieve.return_value = SimpleNamespace(
            status="succeeded",
            currency="sek",
            amount=24998,
            amount_received=24998,
            metadata={"user_id": str(self.user.id)},
        )

        self.login()
        self.create_cart_item(quantity=2)

        order = Order.objects.create(
            user=self.user,
            full_name="Joe Example",
            email="joe@example.com",
            phone="0701234567",
            address1="Test Street 1",
            address2="",
            city="Stockholm",
            postcode="11122",
            country="SE",
            subtotal=Decimal("199.98"),
            tax=Decimal("50.00"),
            total=Decimal("249.98"),
            stripe_payment_intent_id="pi_success_123",
            stripe_currency="sek",
            stripe_amount=24998,
            is_paid=False,
        )

        session = self.client.session
        session["checkout_shipping"] = {
            "full_name": "Joe Example",
            "email": "joe@example.com",
            "phone": "0701234567",
            "address1": "Test Street 1",
            "address2": "",
            "city": "Stockholm",
            "postcode": "11122",
            "country": "SE",
        }
        session["pending_order_id"] = order.id
        session["expected_payment_intent_id"] = "pi_success_123"
        session["expected_payment_amount"] = 24998
        session["expected_payment_currency"] = "sek"
        session.save()

        response = self.client.get(
            reverse("cart:success") + "?payment_intent=pi_success_123",
        )

        order.refresh_from_db()
        self.assertTrue(order.is_paid)
        self.assertEqual(CartItem.objects.count(), 0)

        session = self.client.session
        self.assertNotIn("checkout_shipping", session)
        self.assertNotIn("pending_order_id", session)
        self.assertNotIn("expected_payment_intent_id", session)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(
                "orders:detail",
                kwargs={"order_number": order.order_number},
            ) + "?paid=1",
        )

    @patch("cart.views.stripe.PaymentIntent.retrieve")
    def test_success_redirects_when_payment_intent_does_not_match_session(
        self,
        mock_retrieve,
    ):
        self.login()
        self.create_cart_item(quantity=1)

        order = Order.objects.create(
            user=self.user,
            full_name="Joe Example",
            email="joe@example.com",
            phone="0701234567",
            address1="Test Street 1",
            address2="",
            city="Stockholm",
            postcode="11122",
            country="SE",
            subtotal=Decimal("99.99"),
            tax=Decimal("25.00"),
            total=Decimal("124.99"),
            stripe_payment_intent_id="pi_expected_123",
            stripe_currency="sek",
            stripe_amount=12499,
            is_paid=False,
        )

        session = self.client.session
        session["checkout_shipping"] = {
            "full_name": "Joe Example",
            "email": "joe@example.com",
            "phone": "0701234567",
            "address1": "Test Street 1",
            "address2": "",
            "city": "Stockholm",
            "postcode": "11122",
            "country": "SE",
        }
        session["pending_order_id"] = order.id
        session["expected_payment_intent_id"] = "pi_expected_123"
        session["expected_payment_amount"] = 12499
        session["expected_payment_currency"] = "sek"
        session.save()

        response = self.client.get(
            reverse("cart:success") + "?payment_intent=pi_wrong_999",
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cart:payment"))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                str(message)
                == "Payment verification failed. Please try again."
                for message in messages
            )
        )
