from django.urls import path
from .views import ping, products_list

urlpatterns = [
    path('ping/', ping, name='products-ping'),
    path('', products_list, name='products-list')
]