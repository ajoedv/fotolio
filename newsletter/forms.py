from django import forms
from .models import NewsletterSubscriber


class NewsletterSubscribeForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
