from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('register', views.register, name='register'),
    path('ebooks/', views.ebook_detail, name='ebook_detail'),
    path('library/user/', views.user_profile, name='user_profile'),
    path('recommendations/', views.book_recommendation_list, name='book_recommendation_list'),
    path('downloaded/list/', views.ebook_download_list, name='ebook_download_list'),
    path('history/', views.ebook_history_list, name='ebook_history_list'),
    path('search/books/', views.search_books, name='search_books'),
]