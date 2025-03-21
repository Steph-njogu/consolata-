from django.shortcuts import render,redirect
from django.contrib.auth import logout
from . models import Index
from blogs.models import NewsArticle, Category


#users can choose to logout after login.
def logout_view(request):
    logout(request)
    return redirect ('users:login')

def home_view(request):
    categories = Category.objects.all()
    latest_news = NewsArticle.objects.all().order_by('-date_added')[:4]  

    context = {
        'categories': categories,
        'latest_news': latest_news,
    }

    return render(request, 'home/home.html', context)