from django import forms
from django.core.exceptions import ValidationError
from .models import User
import re


class Step1Form(forms.Form):
    first_name = forms.CharField(
        max_length=200, label='First Name', widget=forms.TextInput(
            attrs={'placeholder': 'Enter First Name'}
        )
    )
    
    last_name = forms.CharField(
        max_length=200, label="Last Name", widget=forms.TextInput(
            attrs={'placeholder': 'Enter Last Name'}
        )
    )

class Step2Form(forms.Form):
    username = forms.CharField(
        max_length=200, 
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    
    profile_pic = forms.ImageField(
        required=False,  
        label="Profile Picture", 
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(f'The username "{username}" is already in use.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class Step3Form(forms.Form):
    email = forms.EmailField(max_length=200, label="Email Address", 
                            widget=forms.EmailInput(attrs={'placeholder':'Enter your Email'}))
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("The email {email} already in use.")
        
        return email
    
    
    phone = forms.CharField(max_length=15, label="Phone Number",
                            widget=forms.TextInput(attrs={'placeholder':'Enter phone number'}))
    

    def clean_phone(self):
        # Clean the phone number field and ensure it's unique
        phone = self.cleaned_data.get('phone')
        if phone:
            if User.objects.filter(phone=phone).exists():  # Check if the phone number already exists
                raise ValidationError(f"The phone number {phone} is already in use.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        # You can perform additional cross-field validation if needed here
        return cleaned_data


class Step4Form(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
                               label="Password",
                               min_length=8,
                               help_text="Password must be at least 8 characters long.")
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
                                       label="Confirm Password")
  

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if not re.search(r'[A-Z]', password):  # At least one uppercase letter
                raise ValidationError("Password must contain at least one uppercase letter.")
            if not re.search(r'[0-9]', password):  # At least one number
                raise ValidationError("Password must contain at least one number.")
            if not re.search(r'[@$!%*?&]', password):  # At least one special character
                raise ValidationError("Password must contain at least one special character.")
        return password


