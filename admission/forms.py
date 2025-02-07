from django import forms
from .models import AdmissionStudent, AdmissionStaff
from django.contrib.auth.hashers import make_password

class AdmissionStudentForm(forms.ModelForm):
    registration_no = forms.CharField(
        label='Registration No.',
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
        if registration_no:
            if AdmissionStudent.objects.filter(registration_no=registration_no).exists():
                raise forms.ValidationError(f"The registration number {registration_no} is already in use.")
            elif not (6000 <= int(registration_no) <= 7000):  # assuming registration_no is a number
                raise forms.ValidationError("Registration number must be between 6000 and 7000.")
        return registration_no

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        # Hash the password before saving
        cleaned_data['password'] = make_password(password)
        return cleaned_data


class AdmissionStaffForm(forms.ModelForm):
    staff_no = forms.CharField(
        label='Staff No.',
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
        if staff_no:
            if AdmissionStaff.objects.filter(staff_no=staff_no).exists():
                raise forms.ValidationError(f"The staff number {staff_no} is already in use.")
        return staff_no

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        # Hash the password before saving
        cleaned_data['password'] = make_password(password)
        return cleaned_data
