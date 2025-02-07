from . models import Profile, Room, RoomAssignment
from users.models import User
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'bio', 'seminary_attended']

    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    seminary_attended = forms.CharField(max_length=300, required=False)

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_block', 'room_number']

class RoomAssignmentForm(forms.ModelForm):
    class Meta:
        model = RoomAssignment
        fields = ['room', 'user', 'end_date']

    def __init__(self, *args, **kwargs):
        super(RoomAssignmentForm, self).__init__(*args, **kwargs)
        
        # Limit users to only verified users in the dropdown
        self.fields['user'].queryset = User.objects.filter(seminarian__is_verified=True)

