from django import forms
from django_countries.widgets import CountrySelectWidget

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "display_name",
            "phone",
            "shipping_full_name",
            "address_line1",
            "address_line2",
            "city",
            "postcode",
            "country",
            "avatar",
        ]
        widgets = {
            "display_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Display name",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone number",
                }
            ),
            "shipping_full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Full name",
                }
            ),
            "address_line1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Address line 1",
                }
            ),
            "address_line2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Address line 2 (optional)",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City",
                }
            ),
            "postcode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Postcode",
                }
            ),
            "country": CountrySelectWidget(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = [
            "display_name",
            "phone",
            "shipping_full_name",
            "address_line1",
            "city",
            "postcode",
            "country",
        ]
        for name in required_fields:
            if name in self.fields:
                self.fields[name].required = True

        if "address_line2" in self.fields:
            self.fields["address_line2"].required = False
