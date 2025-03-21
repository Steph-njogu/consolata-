from django.shortcuts import render, redirect, get_object_or_404
from .models import AdmissionStaff, AdmissionStudent
from .forms import AdmissionStudentForm, AdmissionStaffForm
from datetime import datetime
from django.contrib import messages
from users.models import User
from django.contrib.auth.decorators import login_required


def home(request):
    
    return render(request, 'admission/home.html')

@login_required
def admission_student(request):
    # Check if the user already has a student record
    if AdmissionStudent.objects.filter(user=request.user).exists():
        return redirect('library:home')

    if request.method == 'POST':
        form = AdmissionStudentForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            try:
                # Pass the user explicitly to the save() method
                form.save(user=request.user)
                return redirect('library:home')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = AdmissionStudentForm(initial={'user': request.user})

    context = {'form': form}
    return render(request, 'admission/admission.html', context)


# Staff registration to the portal
@login_required
def admission_staff(request):
    
    # Check if the user already has a staff record
    if AdmissionStaff.objects.filter(user=request.user).exists():
        return redirect('library:home')
    
    if request.method == 'POST':
        form = AdmissionStaffForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            try:
                form.save(user=request.user)
                # Redirect after a successful registration
                return redirect('library:home')
            except ValueError as e:
                 form.add_error(None, str(e))
    else:
        form = AdmissionStaffForm(initial={'user': request.user})

    context = {'form': form}
    return render(request, 'admission/admission_staff.html', context)
