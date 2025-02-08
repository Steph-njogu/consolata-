from django import forms
from .models import AdmissionStudent, AdmissionStaff
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator

# Validators for input fields
registration_validator = RegexValidator(r'^\d{4,6}$', 'Enter a valid registration number (4-6 digits).')
staff_no_validator = RegexValidator(r'^[A-Z]{2}\d{4}$', 'Enter a valid staff number (e.g., ST1234).')

class AdmissionStudentForm(forms.ModelForm):
    registration_no = forms.CharField(
        label='Registration No.',
        validators=[registration_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Enter your registration number'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    class Meta:
        model = AdmissionStudent
        fields = ['registration_no', 'password']

    def clean_registration_no(self):
        registration_no = self.cleaned_data.get('registration_no')
        if AdmissionStudent.objects.filter(registration_no=registration_no).exists():
            raise forms.ValidationError(f"The registration number {registration_no} is already in use.")
        elif not (4000 <= int(registration_no) <= 7000): 
            raise forms.ValidationError("Registration number must be between 4000 and 7000.")
        return registration_no

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"]) 
        if commit:
            user.save()
        return user

class AdmissionStaffForm(forms.ModelForm):
    staff_no = forms.CharField(
        label='Staff No.',
        validators=[staff_no_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Enter your staff number'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    class Meta:
        model = AdmissionStaff
        fields = ['staff_no', 'password']

    def clean_staff_no(self):
        staff_no = self.cleaned_data.get('staff_no')
        if AdmissionStaff.objects.filter(staff_no=staff_no).exists():
            raise forms.ValidationError(f"The staff number {staff_no} is already in use.")
        return staff_no

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # Hash password correctly
        if commit:
            user.save()
        return user
