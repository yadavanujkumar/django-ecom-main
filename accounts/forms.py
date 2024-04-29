from django import forms
from .models import WebsiteRating

class WebsiteRatingForm(forms.ModelForm):
    class Meta:
        model = WebsiteRating
        fields = ['rating']