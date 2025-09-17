from django.urls import path
from .views import products_list, ping, product_detail

app_name = 'products'

urlpatterns = [
    path('ping/', ping, name='ping'),
    path('', products_list, name='list'),
    path('<int:pk>/', product_detail, name='detail'),
]