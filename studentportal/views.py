from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import Step1Form, Step2Form
from admission.models import AdmissionStudent
from . models import ExamsResult

def examresult_view(request):
    results = ExamsResult.objects.all().order_by('-date_added')
    context = {'results' : results }
    return render (request, 'studentportal/examresult.html', context)


def step1(request):
    if request.method == 'POST':
        form = Step1Form(request.POST)
        if form.is_valid():
            # Save the session data for Step 1
            form.save(request)
            return redirect('studentportal:step2')  # Redirect to Step 2 page
    else:
        form = Step1Form()

    return render(request, 'studentportal/step1.html', {'form': form})




def step2(request):
    if not request.user.is_authenticated:
        return redirect('users:login')  # Redirect to login page if the user is not authenticated

    # Retrieve session data from Step 1
    campus_id = request.session.get('campus')
    department_id = request.session.get('department')
    year_id = request.session.get('year')
    semester_id = request.session.get('semester')

    # Get the logged-in user (student)
    user = request.user

    if request.method == 'POST':
        form = Step2Form(user=user, campus_id=campus_id, department_id=department_id, semester_id=semester_id, data=request.POST)
        if form.is_valid():
            # Save the course registration
            form.save(campus_id=campus_id, department_id=department_id, year_id=year_id, semester_id=semester_id)
            
            # Show success message and redirect
            messages.success(request, "Course registration successful!")
            return redirect('sudentportal:success_url')  # Redirect to a success page
    else:
        form = Step2Form(user=user, campus_id=campus_id, department_id=department_id, semester_id=semester_id)

    return render(request, 'studentportal/step2.html', {'form': form})

# sucess page
def success_url(request, slug_student):
    profile = get_object_or_404(AdmissionStudent, slug = slug_student)
    context = {'profile' : profile }
    return render (request,'studentportal/success_url.html', context)
