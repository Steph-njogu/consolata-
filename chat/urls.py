from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('thread/', views.thread_list, name='thread_list'),  # Thread list
    path('thread/<slug:thread_slug>/', views.thread_detail, name='thread_detail'),
    path('chat/', views.create_thread, name='create_thread'),  # Create thread
    

]
