from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns= [
    path('timetable/', views.timetable_view, name='timetable_view'),
    path('<slug:slug_entry>/', views.timetable_detail, name='timetabe_detail'),
]