from django import forms
from .models import Event, Diary, Calendar
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'color', 'location', 'latitude', 'longitude']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Diary Form
class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['name', 'document', 'image']
        widgets = {
            'date_added': forms.DateInput(attrs={'type': 'date'}),
        }

# Calendar Form
class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['event', 'note', 'highlight_date']
        widgets = {
            'highlight_date': forms.DateInput(attrs={'type': 'date'}),
        }

