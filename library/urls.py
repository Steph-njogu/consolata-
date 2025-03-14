from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/library/', views.register, name='register'),
    path('ebook/<slug:slug>/', views.ebook_detail, name='ebook_detail'),
    path('categories/list/', views.category_list, name='category_list'),
    path('search/books/', views.search_books, name='search_books'),
    path('history/', views.ebook_history_list, name='ebook_history_list'),
    path('notes/', views.notes_list, name='notes_list'),
    path('details/int:id/slug:slug', views.notes_detail, name='notes_detail')
]