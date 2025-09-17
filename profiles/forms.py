from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "phone", "default_shipping_address", "avatar"]
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "default_shipping_address": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }