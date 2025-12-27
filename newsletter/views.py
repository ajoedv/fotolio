from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .forms import NewsletterSubscribeForm
from .models import NewsletterSubscriber


@require_POST
def subscribe(request):
    form = NewsletterSubscribeForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Please enter a valid email.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    email = form.cleaned_data["email"].strip().lower()

    obj, created = NewsletterSubscriber.objects.get_or_create(email=email)

    if created:
        messages.success(request, "Subscribed! Welcome to Fotolio updates.")
    else:
        messages.info(request, "You're already subscribed.")

    return redirect(request.META.get("HTTP_REFERER", "/"))
