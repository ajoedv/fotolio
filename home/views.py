from django.contrib import messages
from django.shortcuts import redirect, render

from products.models import Product

from .forms import ContactMessageForm


def index(request):
    """A view to return the index page."""
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

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully.")
            return redirect("contact")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ContactMessageForm()

    context = {
        "teaser_products": teaser_products,
        "form": form,
    }
    return render(request, "home/contact.html", context)
