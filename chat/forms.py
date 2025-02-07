from django import forms
from .models import Reply,Thread
from users.models import User

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['author','image', 'vedio', 'document', 'content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

