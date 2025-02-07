from django.db import models
from users.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.SlugField(max_length=200, blank=True)



    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        original_slug = self.slug
        counter = 1
        while Category.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
        counter += 1
    
        super().save(*args, **kwargs)

class NewsArticle(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    tags = TaggableManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    vedio = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.DRAFT
    )
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        original_slug = self.slug
        counter = 1
        while NewsArticle.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
        counter += 1
    
        super().save(*args, **kwargs)


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
    