from django import forms
from .models import WebsiteRating

class WebsiteRatingForm(forms.ModelForm):
    class Meta:
        model = WebsiteRating
        fields = ['rating']
        
        
from django import forms
from django.contrib.auth.models import User
from accounts.models import Address

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_line', 'second_line', 'zip_code', 'city', 'state']