from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.HiddenInput(
            attrs={"id": "id_rating"}
        )
    )

    comment = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Write your review..."
            }
        )
    )

    class Meta:
        model = ProductReview
        fields = ["rating", "comment"]
