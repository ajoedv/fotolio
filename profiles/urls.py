from django.urls import path
from .views import profile

app_name = "profiles"

urlpatterns = [
    path("", profile, name="profile"),
]