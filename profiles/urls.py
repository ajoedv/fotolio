from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.profile_view, name="profile"),
    path("edit/", views.edit_profile, name="edit"),
    path("delete/", views.delete_profile, name="delete"),
]
