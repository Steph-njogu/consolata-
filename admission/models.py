from django.db import models
from django.utils.text import slugify
from users.models import User  
from django.contrib.auth.hashers import make_password

# AdmissionStudent model
class AdmissionStudent(models.Model):
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=128) 
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Ensure slug uniqueness by checking if it already exists and appending a number if necessary
        if not self.slug:
            self.slug = slugify(self.registration_no)
        
        original_slug = self.slug
        counter = 1
        max_retries = 100  # Prevent infinite loop
        while AdmissionStudent.objects.filter(slug=self.slug).exists() and counter <= max_retries:
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        
        if counter > max_retries:
            raise ValueError("Unable to generate a unique slug after 100 retries.")

        # Hash password before saving
        if self.password:
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.registration_no

    class Meta:
        db_table = 'admission_student'  # Specify the table name
        ordering = ['registration_no']  # Order by registration number


# AdmissionStaff model
class AdmissionStaff(models.Model):
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    staff_no = models.CharField(max_length=200, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)  # Reduced length for hashed password
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Ensure slug uniqueness by checking if it already exists and appending a number if necessary
        if not self.slug:
            self.slug = slugify(self.staff_no)
        
        original_slug = self.slug
        counter = 1
        max_retries = 100  # Prevent infinite loop
        while AdmissionStaff.objects.filter(slug=self.slug).exists() and counter <= max_retries:
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        
        if counter > max_retries:
            raise ValueError("Unable to generate a unique slug after 100 retries.")

        # Hash password before saving
        if self.password:
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.staff_no

    class Meta:
        db_table = 'admission_staff'  # Specify the table name
        ordering = ['staff_no']  # Order by staff number
