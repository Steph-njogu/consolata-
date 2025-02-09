from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import Step1Form, Step2Form
from admission.models import AdmissionStudent
from . models import ExamsResult
from django.http import HttpResponse
from PyPDF2 import PdfReader

def examresult_view(request):
    results = ExamsResult.objects.all().order_by('-date_added')
    context = {'results' : results }
    return render (request, 'studentportal/examresult.html', context)

#this should open the document afetr download.
def results_view(request, slug_result):
    result = get_object_or_404(ExamsResult, slug = slug_result)
    
   
    if result.document:
        # Process PDF (e.g., extract text)
        document_path = result.document.path
        
        try:
            # Open the PDF file and read content (optional: extract text or metadata)
            with open(document_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ''
                # Extract text from each page
                for page in pdf_reader.pages:
                    text += page.extract_text()

            # Optional: You can process the text (log it, save it, etc.)
            print(text)  # For example, just print the extracted text to the console
        except Exception as e:
            print(f"Error processing PDF: {e}")

        # Serve the file for download
        with open(document_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{result.document.title}"'
            return response
    
    else:
        return redirect('studentportal:examresult_view')



#students course registration 
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



#students course registration 
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



# sucess after login and registration page
def success_url(request, slug_student):
    profile = get_object_or_404(AdmissionStudent, slug = slug_student)
    context = {'profile' : profile }
    return render (request,'studentportal/success_url.html', context)
