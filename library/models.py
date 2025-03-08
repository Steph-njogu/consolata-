from django.db import models
from users.models import User
import taggit.managers
from django.utils.text import slugify
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Publisher(models.Model):
    name = models.CharField(max_length=200)
    contact_info = models.CharField(blank=True, max_length=200, null=True)
    website = models.URLField(blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Publisher, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class EBook(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    genre = models.CharField(blank=True, max_length=100, null=True)
    language = models.CharField(blank=True, max_length=50, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True, null=True)
    e_book_file = models.FileField(blank=True, null=True, upload_to='ebooks/')
    cover_image = models.ImageField(blank=True, null=True, upload_to='book_covers/')
    slug = models.SlugField(blank=True, unique=True)
    
    # ForeignKey fields
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True, related_name="books")

    # Tags field using Taggit
    tags = taggit.managers.TaggableManager(help_text="A comma-separated list of tags.", verbose_name="Tags")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(EBook, self).save(*args, **kwargs)

    def __str__(self):
        return self.title




class LibraryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    membership_date = models.DateField(auto_now_add=True)
    preferences = models.TextField(blank=True, null=True)
    wishlist = models.ManyToManyField(EBook, blank=True, related_name='wishlist')

    def __str__(self):
        return self.user.username



class EBookLoan(models.Model):
    STATUS_CHOICES = [
        ('Reserved', 'Reserved'),
        ('Picked up', 'Picked up'),
    ]
    
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, default=None, null=True)
    returned = models.BooleanField(default=False)
    late_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    
    # ForeignKey fields
    ebook = models.ForeignKey(EBook, on_delete=models.CASCADE)
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ebook.title} Loan"
    


class EBookHistory(models.Model):
    ACTION_CHOICES = [
        ('Read', 'Read'),
        ('Downloaded', 'Downloaded'),
        ('Loaned', 'Loaned'),
    ]

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)

    # ForeignKey fields
    ebook = models.ForeignKey(EBook, on_delete=models.CASCADE)
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.action} by {self.user}"



class EBookDownload(models.Model):
    download_date = models.DateTimeField(auto_now_add=True)

    # ForeignKey fields
    ebook = models.ForeignKey(EBook, on_delete=models.CASCADE)
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Download by {self.user}"