from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Product
from .constants import BASE_SIZE_LABEL


def ping(request):
    return HttpResponse("Products route OK")


def products_list(request):
    products = (
        Product.objects
        .select_related("category")
        .order_by("name")
    )
    teaser_products = Product.objects.order_by("?")[:10]

    context = {
        "products": products,
        "teaser_products": teaser_products,
    }
    return render(request, "products/list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    teaser_products = (
        Product.objects
        .exclude(pk=product.pk)
        .order_by("?")[:10]
    )

    context = {
        "product": product,
        "base_size": BASE_SIZE_LABEL,
        "teaser_products": teaser_products,
    }
    return render(request, "products/detail.html", context)
