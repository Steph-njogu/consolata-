from django.db import models
from users.models import User
from django.utils.text import slugify

# Create your models here.


class Thread(models.Model):
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    image = models.ImageField(upload_to='chats/Y%/M%/d%/', blank=True, null=True)
    vedio = models.FileField(upload_to='chats/Y%/M%/d%/', blank=True, null=True)
    document = models.FileField(upload_to='chats/Y%/M%/d%/', blank=True, null=True)
    content = models.TextField() 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.author)
        original_slug = self.slug
        counter = 1
        while Thread.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
        counter += 1
    
        super().save(*args, **kwargs)

    def __str__(self):
        return self.author.username
    
class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} to {self.thread}"


