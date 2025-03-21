from django import forms
from .models import Order
from users.models import User

class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), required=True)
    city = forms.CharField(max_length=100, required=True)

    def load_from_user(self, user):
        """Pre-fill form fields from the User model."""
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['phone'].initial = user.phone if hasattr(user, 'phone') else ''
