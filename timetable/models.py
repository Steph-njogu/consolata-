from django.db import models
from django.utils.text import slugify

# Create your models here.
class Timetable(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    document = models.FileField(upload_to='documents/',  blank=True, null=True)
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)


    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

