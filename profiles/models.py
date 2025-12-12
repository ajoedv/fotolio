from django.db import models
from django.contrib.auth.models import User


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
    default_shipping_address = models.TextField(
        blank=True,
        verbose_name="Default shipping address",
        help_text="Used to prefill your details at checkout.",
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
