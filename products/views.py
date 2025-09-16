from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def ping(request):
    return HttpResponse("Products route OK")

def products_list(request):
    products = Product.objects.select_related('category').order_by('name')
    return render(request, 'products/list.html', {'products': products})