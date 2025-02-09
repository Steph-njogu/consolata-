# forms.py
from django import forms
from users.models import User
from .models import LibraryUser

class LibraryUserRegistrationForm(forms.Form):
    email = forms.EmailField(required=True,label='Email', widget=forms.Textarea(attrs={'palceholder' : 'Enter your email address'}))
    
    class Meta:
        model = User
        fields = ['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            library_user = LibraryUser(user=user)
            library_user.save()
        return user







