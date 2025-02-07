from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Diary
from .forms import  DiaryForm, EventForm
from django.utils.timezone import now
from django.http import JsonResponse
import os
from .utils import extract_text_from_pdf
from django.contrib.auth.decorators import login_required, user_passes_test


# Calendar view 
@login_required
def event_view(request):
    current_month = now().month
    events = Event.objects.filter(event_date__month=current_month)
    return render(request, 'events/calendar_view.html', {'events': events})


#list of all diaries
@login_required
def diaries_view(request):
    diaries = Diary.objects.order_by('-date_added')
    context = {'diaries':diaries}
    return render (request, 'events/diary_view.html', context)


# Diary view with error handling
@login_required
def diary_view(request, diary_slug):
    # Fetch the specific diary by slug
    diary = get_object_or_404(Diary, slug=diary_slug)

    # Initialize the document text
    document_text = None

    # Check if the diary has an attached document
    if diary.document:
        file_path = diary.document.path  # This gives the full file path

        # Check if the file exists
        if os.path.exists(file_path):
            file_extension = os.path.splitext(file_path)[-1].lower()

            # Extract text based on the file extension
            if file_extension == ".pdf":
                try:
                    document_text = extract_text_from_pdf(file_path)
                except Exception as e:
                    document_text = f"Error extracting text from PDF: {str(e)}"
            elif file_extension == ".txt":
                # Read the text file and return its content
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        document_text = file.read()
                except Exception as e:
                    document_text = f"Error reading text file: {str(e)}"
            else:
                document_text = "Unsupported file format."
        else:
            document_text = "File not found."
    else:
        document_text = "No document available for this diary."

    return render(request, 'events/diary_view.html', {'diary': diary, 'document_text': document_text})



# Add or update diary (only for admin users)
@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_diary(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.user = request.user  
            diary.save()
            return redirect('events:diaries_view')  
    else:
        form = DiaryForm()

    context = {'form': form}
    return render(request, 'events/add_diary.html', context)



# Event detail view with comment handling
@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_event(request):
    
    # Handling comment section
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.event = request.user
            new_event.save()
            return redirect('events:event_view')
    else:
        form = EventForm()

    context = {'form': form}
    return render(request, 'events/event_detail.html', context)



