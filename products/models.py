from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(
        max_length=254,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name or self.name


class Product(models.Model):
    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    sku = models.CharField(
        max_length=254,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    image_url = models.URLField(
        max_length=1024,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product} - {self.user} ({self.rating}/5)"
