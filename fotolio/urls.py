"""
URL configuration for fotolio project.
"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

# Error handlers


def custom_page_not_found(request, exception):
    """Custom 404 page."""
    return render(request, "404.html", status=404)


def custom_server_error(request):
    """Custom 500 page."""
    return render(request, "500.html", status=500)


# URL patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("home.urls")),
    path("products/", include("products.urls")),
    path("profile/", include("profiles.urls", namespace="profiles")),
    path("cart/", include("cart.urls", namespace="cart")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)

handler404 = "fotolio.urls.custom_page_not_found"
handler500 = "fotolio.urls.custom_server_error"
