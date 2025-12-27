from django.urls import path
from .views import subscribe


app_name = "newsletter"

urlpatterns = [
    path("subscribe/", subscribe, name="subscribe"),
]
