from django.db import models
from users.models import User

# Create your models here.
class Profile(models.Model):

    ROLE_CHOICES = [
        ('SEMINARIAN', 'Seminarian'),
        ('ALUMNI', 'Alumni'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seminarian")
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank = True, null=True)
    seminary_attended = models.CharField(max_length=300, blank=True, null=True)

    

    def __str__(self):
        return f"{self.user} ({self.role})"


class Room(models.Model):
    room_number = models.IntegerField()
    room_block = models.CharField(max_length=200)
    
 

    
    def __str__(self):
        return f"{self.room_number}- {self.room_block}"


#Rooms assigning 
class RoomAssignment(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='assignments')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='room_assignments')
    start_date = models.DateField(auto_now_add=True)  # The date the room assignment starts
    end_date = models.DateField()    # The date the room assignment ends

    def __str__(self):
        return f"{self.room.room_number} assigned to {self.user} from {self.start_date} to {self.end_date}"

    class Meta:
        unique_together = ('room', 'start_date', 'end_date')

