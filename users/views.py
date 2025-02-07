from django.shortcuts import render,redirect,get_object_or_404
from .forms import Step1Form, Step2Form, Step3Form,Step4Form
from .models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required



#Registeration view: this allows users to register in the web page if its a new user.
def register1_view(request):
    if request.method == 'POST':
        form = Step1Form(request.POST)
        if form.is_valid():
            request.session['step1_data'] = form.cleaned_data
            return redirect('users:register2_view')
    else:
        form = Step1Form()
    return render(request, 'users/register1_view.html', {'form':form})

# redirect if step1_data is not in session
def register2_view(request):
    if 'step1_data' not in request.session:
        return redirect('users:register1_view')  
    if request.method == 'POST':
        form = Step2Form(request.POST)
        if form.is_valid():
            request.session['step2_data'] = form.cleaned_data
            return redirect('users:register3_view')
    else:
        form = Step2Form()
    return render(request, 'users/register2_view.html', {'form': form})




def register3_view(request):
    if 'step1_data' not in request.session or 'step2_data' not in request.session:
        return redirect ('users:register1_view')
    if request.method == 'POST':
        form = Step3Form(request.POST)
        if form.is_valid():
            request.session['step3_data'] = form.cleaned_data
            return redirect('users:register4_view')
    else:
        form = Step3Form()
    return render(request, 'users/register3_view.html', {'form':form})


# redirect to login after registration
def register4_view(request):
    if 'step1_data' not in request.session or 'step2_data' not in request.session or 'step3_data' not in request.session:
        return redirect('users:register1_view')  # fix missing session data
    if request.method == 'POST':
        form = Step4Form(request.POST)
        if form.is_valid():
            step1_data = request.session.pop('step1_data', {})
            step2_data = request.session.pop('step2_data', {})
            step3_data = request.session.pop('step3_data', {})
            step4_data = form.cleaned_data
            user = User(
                first_name=step1_data.get('first_name'),
                last_name=step1_data.get('last_name'),
                username=step2_data.get('username'),
                profile_pic=step2_data.get('profile_pic'),
                email=step3_data.get('email'),
                phone=step3_data.get('phone'),
            )
            user.set_password(step4_data.get('password'))
            user.save()
            login(request, user)
            return redirect('home:home')  
    else:
        form = Step4Form()
    return render(request, 'users/register4_view.html', {'form': form})


@login_required
def profile_view(request, slug_user):
    user = get_object_or_404(User, slug=slug_user)

    return render(request, 'users/profile_view.html', {'user': user})


