from django import forms
from django.contrib import admin
from .models import Profile, Room, RoomAssignment

# admin for profile membership
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_verified', 'bio', 'seminary_attended']
    list_filter = ['role', 'is_verified']
    actions = ['approve_profile', 'reject_profile']

    def approve_profile(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, "Selected profiles have been approved.")

    def reject_profile(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, "Selected profiles have been rejected.")

    approve_profile.short_description = "Approve selected profiles"
    reject_profile.short_description = "Reject selected profiles"


admin.site.register(Profile, ProfileAdmin)


# admin model for rooms checker
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_block', 'room_number']
    search_fields = ['room_block']


admin.site.register(Room, RoomAdmin)


class RoomAssignmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'room']
    search_fields = ['user', 'room']

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        user = cleaned_data.get('user')

        # Check if user is provided
        if user:  
            # Check if the user is approved
            if not user.is_approved:  # Assuming 'user' is a Profile object with 'is_approved'
                raise forms.ValidationError(f"{user} is not an approved member and cannot be assigned a room.")

            # Check if the room is already occupied by another user
            if room:  # Ensure room is provided
                existing_assignment = RoomAssignment.objects.filter(room=room).first()  # Find an existing assignment for the room
                
                if existing_assignment:  # If there's already an assignment for the room
                    raise forms.ValidationError(f"Room {room.room_number} in block {room.room_block} is already assigned to {existing_assignment.user}.")

        return cleaned_data


admin.site.register(RoomAssignment, RoomAssignmentAdmin)
