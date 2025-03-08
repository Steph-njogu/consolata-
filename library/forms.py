from django import forms
from users.models import User
from .models import LibraryUser

class LibraryUserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='Email', 
        widget=forms.EmailInput(attrs={'placeholder' : 'Enter your email address'})
    )

    class Meta:
        model = LibraryUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.initial.get('user')  # Get the user passed in context

        # Check if the logged-in user has already registered with this email
        if LibraryUser.objects.filter(user=user).exists():
            raise forms.ValidationError(f"You have already registered with this account.")

        # Check if the email already exists in the LibraryUser model (for other users)
        if LibraryUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f"The email {email} is already in use by another user.")
        
        return email
    
    def save(self, user, commit=True):
        # Check if the logged-in user already has a LibraryUser entry
        if LibraryUser.objects.filter(user=user).exists():
            raise ValueError("This user has already registered.")

        # Create the LibraryUser instance and associate it with the User
        library_user = super().save(commit=False)  # Don't commit yet
        library_user.user = user  # Link LibraryUser to the provided user (which is the logged-in user)
        
        if commit:
            library_user.save()  # Save the LibraryUser instance
        return library_user
