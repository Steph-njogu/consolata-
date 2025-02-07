from django.shortcuts import render, redirect
from .models import Thread
from .forms import ReplyForm, ThreadForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def thread_list(request):
    threads = Thread.objects.all().order_by('-created_at')
    canonical_url = request.build_absolute_uri(request.path)
    context = {'canonical_url':canonical_url, 'threads': threads}
    return render(request, 'chat/category_list.html', context)



@login_required
def thread_detail(request, thread_slug):
    thread = Thread.objects.get(slug=thread_slug)
    replies = thread.replies.all().order_by('-created_at')
    
#this creates the reply base
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.save()
            return redirect('chat:thread_detail', thread_slug=thread.slug)
    else:
        form = ReplyForm()
    
    canonical_url = request.build_absolute_uri(request.path)

    context = {'canonical_url':canonical_url, 'thread': thread, 'replies': replies, 'form': form}
    return render(request, 'chat/thread_detail.html', context)


# creating or initializing a new chat
@login_required
def create_thread(request):
     
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat:thread_list')  # Redirect to the thread_list page
    else:
        form = ThreadForm()
    
    context = {'form': form}
    return render(request, 'chat/create_thread.html', context)


