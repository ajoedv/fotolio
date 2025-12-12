from django.db import models


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
