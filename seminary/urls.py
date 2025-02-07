from . import views
from django.urls import path
from django.contrib.auth.views import LoginView

app_name = 'seminary'

urlpatterns = [
    path('request/', views.request_membership, name='request_membership'),
    path('portal/', views.seminary_portal, name='seminary_portal'),
    path('assign/', views.assign_room, name='assign_room'),
    path('room/', views.room_details, name='room_details'),
]