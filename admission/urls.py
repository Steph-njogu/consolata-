from django.urls import path
from . import views 


app_name = 'admission'

urlpatterns = [
    path('reg/student/portal/', views.admission_student, name='admission_student' ),
    path('reg/staff/portal/', views.admission_staff, name='admission_staff'),
    path('home/', views.home, name='home'),
    
]