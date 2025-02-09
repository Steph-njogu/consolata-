from django.db import models
from django.utils.text import slugify
from admission.models import AdmissionStudent
from course.models import Campus, Department, YearOfStudy, Semester, Field, Course
from django.core.exceptions import ValidationError

# ExamsResult Model
class ExamsResult(models.Model):
    student = models.ForeignKey(AdmissionStudent, on_delete=models.CASCADE)  # Related to the student
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    document = models.FileField(upload_to='documents/pdfs/', blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.registration_no} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# CourseRegistration Model
class CourseRegistration(models.Model):
    student = models.ForeignKey(AdmissionStudent, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.ForeignKey(YearOfStudy, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='fields')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # student can register for a course only once
        indexes = [
            models.Index(fields=['student', 'course', 'semester']),  # Add index for faster lookups
        ]

    def clean(self):
        """Ensure a student can't register for the same course multiple times in a given semester."""
        if CourseRegistration.objects.filter(
            student=self.student, course=self.course, semester=self.semester
        ).exists():
            raise ValidationError(
                f"{self.student.registration_no} is already registered for {self.course.course_name} in this semester."
            )

    def save(self, *args, **kwargs):
        # Check if the student is already registered for the same course in the semester
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.registration_no} registered for {self.course.course_name} in {self.semester.semester}"

