from django import forms
from .models import Subscriber

class NewsForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']