from django.urls import path
from .views import products_list, ping, product_detail
from . import views

app_name = "products"

urlpatterns = [
    path(
        "ping/",
        ping, name="ping"
    ),
    path(
        "",
        products_list,
        name="list"
    ),
    path(
        "<int:pk>/",
        product_detail,
        name="detail"
    ),
    path(
        "<int:product_id>/reviews/add/",
        views.review_create,
        name="review_add"
    ),
    path(
        "reviews/<int:review_id>/edit/",
        views.review_edit,
        name="review_edit"
    ),
    path(
        "reviews/<int:review_id>/delete/",
        views.review_delete,
        name="review_delete"
    ),
]
