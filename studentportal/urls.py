from django.urls import path
from . import views

app_name = 'studentportal'

urlpatterns = [
    path('student/', views.step1, name='step1'),
    path('registration/', views.step2, name='step2'),
    path('success/<slug:slug_student>/', views.success_url, name='success_url'),
    path('examresult/', views.examresult_view, name='examresult_view'),
]