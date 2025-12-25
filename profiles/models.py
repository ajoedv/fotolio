from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    display_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Display name",
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Phone number",
    )

    shipping_full_name = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Shipping full name",
    )

    address_line1 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Address line 1",
    )

    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Address line 2",
    )

    city = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="City",
    )

    postcode = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="Postcode",
    )

    country = CountryField(
        blank=True,
        verbose_name="Country",
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.user.get_username()
