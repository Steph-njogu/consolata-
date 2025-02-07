from django import forms
from .models import CourseRegistration
from course.models import Campus, Department, YearOfStudy, Semester, Field, Course
from admission.models import AdmissionStudent


class Step1Form(forms.Form):
    campus = forms.ModelChoiceField(queryset=Campus.objects.all(), empty_label="Select a Campus")
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select a Department")
    year = forms.ModelChoiceField(queryset=YearOfStudy.objects.all(), empty_label="Select Year of Study")
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label="Select a Semester")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can limit the choices based on certain logic if needed (e.g., filter by campus, department, etc.)

    def save(self, request):
        # Save the session data for Step 1
        request.session['campus'] = self.cleaned_data['campus'].id
        request.session['department'] = self.cleaned_data['department'].id
        request.session['year'] = self.cleaned_data['year'].id
        request.session['semester'] = self.cleaned_data['semester'].id




class Step2Form(forms.Form):
    field = forms.ModelChoiceField(queryset=Field.objects.all(), empty_label="Select a Field")
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select a Course")
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the logged-in student
        self.student = AdmissionStudent.objects.get(user=user)
        
        # Get session data from Step 1
        campus_id = kwargs.get('campus_id')
        department_id = kwargs.get('department_id')
        semester_id = kwargs.get('semester_id')

        # Filter fields based on session data (department and semester)
        self.fields['field'].queryset = Field.objects.filter(
            semester__id=semester_id,
            department__id=department_id
        )
        
        # Filter courses based on the selected field
        self.fields['course'].queryset = Course.objects.filter(
            field__semester__id=semester_id,
            field__department__id=department_id
        )
    
    def save(self, *args, **kwargs):
        # Save the registration form data
        data = self.cleaned_data
        course_registration = CourseRegistration(
            student=self.student,
            field=data['field'],
            course=data['course'],
            campus_id=kwargs['campus_id'],
            department_id=kwargs['department_id'],
            year_id=kwargs['year_id'],
            semester_id=kwargs['semester_id']
        )
        course_registration.save()
        return course_registration
