from django.db import models
from django.utils.text import slugify
from users.models import User

# Event model
class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField()
    event_date = models.DateField()
    color = models.CharField(max_length=7, null=True, blank=True)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# Diary model
class Diary(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    date_added = models.DateField(auto_now_add=True)
    document = models.FileField(upload_to='documents/Y%/M%/d%/', null=True, blank=True)
    image = models.ImageField(upload_to='pictures/Y%/M%/d%/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Diary, self).save(*args, **kwargs)


# Calendar model
class Calendar(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)
    highlight_date = models.DateField()

    def __str__(self):
        return self.event.title


