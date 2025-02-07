from . import views
from django.urls import path
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView,PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetView

app_name = 'users'

urlpatterns = [
    #This url connects the user to the login page.  
    path('login/', LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('register/step1/', views.register1_view, name='register1_view'),
    path('register/step2/', views.register2_view, name='register2_view'),
    path('register/step3/', views.register3_view, name='register3_view'),
    path('register/step4/', views.register4_view, name='register4_view'),
    path('profile/<slug:slug_user>/', views.profile_view, name='profile'),
    path('password/change/', PasswordChangeView.as_view(template_name = 'users/password_change.html'), name='password_change'),
    path('password/change/done/', PasswordChangeDoneView.as_view(template_name = 'users/password_change_done.html'), name='password_change_done'),
    path('password/reset/', PasswordResetView.as_view(template_name = 'users/password_reset.html'), name='password_reset'),
    path('password/reset/done/', PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/complete/', PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name='password_reset_complete'),
]