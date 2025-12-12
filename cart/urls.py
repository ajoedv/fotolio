from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.detail, name="detail"),
    path("add/<int:product_id>/", views.add_to_cart, name="add"),
    path("update/<int:item_id>/", views.update_item, name="update"),
    path("remove/<int:item_id>/", views.remove_item, name="remove"),
]
