import uuid
from django.db import models
from django.utils.text import slugify
from users.models import User  
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied

def generate_unique_slug(instance, field):
    """Generates a unique slug by appending a UUID"""
    base_slug = slugify(field)
    unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
    return unique_slug

# AdmissionStudent model
class AdmissionStudent(models.Model):
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.user)
        super().save(*args, **kwargs)  

    def verify(self, user):
        """Only allow admin users to verify the student."""
        if not user.is_superuser:
            raise PermissionDenied("You must be an admin to verify a student.")
        self.is_verified = True
        self.save()

    def __str__(self):
        return self.registration_no

    class Meta:
        ordering = ['registration_no']


# AdmissionStaff model
class AdmissionStaff(models.Model):
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    staff_no = models.CharField(max_length=200, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.user)
        super().save(*args, **kwargs)  

    def verify(self, user):
        """Only allow admin users to verify the student."""
        if not user.is_superuser:
            raise PermissionDenied("You must be an admin to verify a staff.")
        self.is_verified = True
        self.save()


    def __str__(self):
        return self.staff_no

    class Meta:
        ordering = ['staff_no']
        