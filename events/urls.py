from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('diary/add/', views.add_diary, name='add_diary'),
    path('calendar/', views.event_view, name='event_view'),
    path('diaries/', views.diaries_view, name= 'diaries_view'),
    
    path('add/events/', views.add_event, name='add_event'),
    path('diary/<slug:diary_slug>/', views.diary_view, name='diary_view'),  
]
