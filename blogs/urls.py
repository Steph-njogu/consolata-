from django.urls import path
from . import views

app_name = 'blogs'  # Add the namespace for the app

urlpatterns = [
    path('news/', views.news_home, name='news_home'),  # News page with pagination
    path('category/<slug:category_slug>/', views.category_news, name='category_news'),  # Category-specific news
    path('news/<slug:news_slug>/', views.news_detail, name='news_detail'),  # Detailed news article
    path('subscribe/', views.subscribe_view, name='subscribe'),  # Newsletter subscription form
    path('subscribed/', views.subscribed, name='subscribed'),  # Confirmation page for subscription
]
