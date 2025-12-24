from django.urls import path

from .views import order_list, order_detail

app_name = "orders"

urlpatterns = [
    path("", order_list, name="list"),
    path("<str:order_number>/", order_detail, name="detail"),
]
