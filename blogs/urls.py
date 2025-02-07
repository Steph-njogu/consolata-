"""
URL configuration for seminaryproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .feeds import LatestFeed

app_name = 'blogs'

urlpatterns = [
    path('rss/', LatestFeed(), name= 'news_rss'),
    path('blogs/', views.news_home, name='news_home'),
    path('category/<slug:category_slug>/', views.category_news, name='category_news'),
    path('news/<slug:news_slug>/', views.news_detail, name='news_detail'),
    path('subscribe/', views.subscribe_view, name='subscribe_view'),  
    path('subscribed/', views.subscribed, name='subscribed'),
]
