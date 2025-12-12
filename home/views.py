from django.shortcuts import render
from products.models import Product


def index(request):
    """ A view to return the index page """
    teaser_products = Product.objects.order_by("?")[:10]
    context = {
        "teaser_products": teaser_products,
    }
    return render(request, "home/index.html", context)


def about(request):
    teaser_products = Product.objects.order_by("?")[:10]
    context = {
        "teaser_products": teaser_products,
    }
    return render(request, "home/about.html", context)


def contact(request):
    teaser_products = Product.objects.order_by("?")[:10]
    context = {
        "teaser_products": teaser_products,
    }
    return render(request, "home/contact.html", context)
