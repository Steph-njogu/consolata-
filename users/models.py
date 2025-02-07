from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# Custom validator for profile picture size
def validate_image_size(image):
    # 5MB limit (5 * 1024 * 1024 bytes)
    max_size = 5 * 1024 * 1024  # 5MB
    if image.file.size > max_size:
        raise ValidationError("Profile picture size must be under 5 MB.")


class User(AbstractUser):
    # Phone number field with validation (at least 9 digits and max 15 digits)
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be between 9 and 15 digits.")]
    )
    
    # Profile picture field with a size validation
    profile_pic = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, validators=[validate_image_size])

    # Slug field for creating URL-friendly strings
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username if self.username else 'Unknown User'
