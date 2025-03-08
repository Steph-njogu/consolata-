from django.shortcuts import render, redirect, get_object_or_404
from .models import AdmissionStaff, AdmissionStudent
from .forms import AdmissionStudentForm, AdmissionStaffForm
from datetime import datetime
from users.models import User


def home(request):
    
    return render(request, 'admission/home.html')


# Student registration to the portal
def admission_student(request):    
    if request.method == 'POST':
        form = AdmissionStudentForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            try:
                new_user = form.save(user=request.user)
                # Redirect after a successful registration
                return redirect('library:home')
            except ValueError:
                 form.add_error(None, "You have already registered with this account.")
    else:
        form = AdmissionStudentForm(initial={'user': request.user})

    context = {'form': form}
    return render(request, 'admission/admission.html', context)


# Staff registration to the portal
def admission_staff(request):
    if request.method == 'POST':
        form = AdmissionStaffForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            try:
                new_user = form.save(user=request.user)
                # Redirect after a successful registration
                return redirect('library:home')
            except ValueError:
                 form.add_error(None, "You have already registered with this account.")
    else:
        form = AdmissionStaffForm(initial={'user': request.user})

    context = {'form': form}
    return render(request, 'admission/admission_staff.html', context)


