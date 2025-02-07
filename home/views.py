from django.shortcuts import render,redirect
from django.contrib.auth import logout
from . models import Index


#users can choose to logout after login.
def logout_view(request):
    logout(request)
    return redirect ('users:login')

def home(request):
    contents = Index.objects.all()
    context = {'contents': contents}
    return render (request, 'home/home.html', context)