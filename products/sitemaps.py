from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.order_by("pk")

    def location(self, obj):
        return reverse("products:detail", args=[obj.pk])
