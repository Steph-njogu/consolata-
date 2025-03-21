from . import views
from django.urls import path
from django.contrib.auth.views import LoginView

app_name = 'home'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),    
]