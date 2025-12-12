from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit"),
    path("profile/delete/", views.delete_profile, name="deletee"),
]
