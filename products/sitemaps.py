from django.contrib.sitemaps import Sitemap

from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return f"/products/{obj.pk}/"
