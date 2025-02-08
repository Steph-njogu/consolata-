from django.urls import path
from . import views 


app_name = 'admission'

urlpatterns = [
    path('reg/student/portal/<slug:student_slug>/', views.admission_student, name='admission_student' ),
    path('reg/staff/portal/<slug:staff_slug>/', views.admission_staff, name='admission_staff'),
    
]