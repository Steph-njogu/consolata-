from django.shortcuts import render, redirect, get_object_or_404
from .models import AdmissionStaff, AdmissionStudent
from .forms import AdmissionStudentForm, AdmissionStaffForm

# Students registration to the portal
def admission_student(request, student_slug):
    student_user = get_object_or_404(AdmissionStudent, slug=student_slug)

    if request.method == 'POST':
        form = AdmissionStudentForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user = request.user  # Associate student with logged-in user
            new_user.save()
            return redirect('admission:home', student_slug=student_user.slug)
    else:
        form = AdmissionStudentForm()

    context = {'student_user': student_user, 'form': form}
    return render(request, 'admission/admission.html', context)

# The staffs registration to the portal
def admission_staff(request, staff_slug):
    staff_user = get_object_or_404(AdmissionStaff, slug=staff_slug)

    if request.method == 'POST':
        form = AdmissionStaffForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user = request.user  # Associate staff with logged-in user
            new_user.save()
            return redirect('admission:home', staff_slug=staff_user.slug)
    else:
        form = AdmissionStaffForm()

    context = {'staff_user': staff_user, 'form': form}
    return render(request, 'admission/admission_staff.html', context)
