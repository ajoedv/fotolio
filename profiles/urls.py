# profiles/urls.py
from django.urls import path
from .views import profile_view, edit_profile

app_name = "profiles"

urlpatterns = [
    path("", profile_view, name="profile"),
    path("edit/", edit_profile, name="edit"),
]