from django.db import models
from django.utils.text import slugify

# University Model
class University(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Campus Model with Choices for Campus Type
class Campus(models.Model):
    CAMPUS_CHOICES = [
        ('Main', 'Main campus'),
        ('Kirinyaga', 'Kirinyaga campus'),
        ('Kisumu', 'Kisumu campus'),
    ]

    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='campuses')
    campus = models.CharField(max_length=20, choices=CAMPUS_CHOICES, default='Main')
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.university.name}-{self.campus}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.campus} - {self.university.name}"


# Department Model within a Campus
class Department(models.Model):
    university = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='departments')
    department_name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.university.campus}-{self.department_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.department_name

# Year of Study Model
class YearOfStudy(models.Model):
    YEARS_OF_STUDY = [
        ('Year1', 'Year 1'),
        ('Year2', 'Year 2'),
        ('Year3', 'Year 3'),
        ('Year4', 'Year 4'),
    ]

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='year_of_study')
    year = models.CharField(max_length=20, choices=YEARS_OF_STUDY, verbose_name="Year of Study")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.department.university}-{self.department.department_name}-{self.year}")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Year of Study"
        verbose_name_plural = "Years of Study"


# Semester Model
class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('Semester1', 'Semester 1'),
        ('Semester2', 'Semester 2'),
    ]

    year = models.ForeignKey(YearOfStudy, on_delete=models.CASCADE, related_name='semesters')
    semester = models.CharField(max_length=30, choices=SEMESTER_CHOICES)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.year.department.department_name}-{self.semester}")
        super().save(*args, **kwargs)


# Field Model
class Field(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='fields')
    field_name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.semester.year.year}-{self.field_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.field_name


# Course Model within a Field
class Course(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='courses')
    course_name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.field.field_name}-{self.course_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name