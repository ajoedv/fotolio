from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from .constants import BASE_SIZE_LABEL  # ← جديد

def ping(request):
    return HttpResponse("Products route OK")

def products_list(request):
    products = Product.objects.select_related('category').order_by('name')
    return render(request, 'products/list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product,
        "base_size": BASE_SIZE_LABEL,
    }
    return render(request, "products/detail.html", context)