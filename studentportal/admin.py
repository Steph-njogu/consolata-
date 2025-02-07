from django.contrib import admin
from .models import ExamsResult, CourseRegistration

class ExamsResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'title',  'date_added')
    search_fields = ('student__registration_no', 'title')
    

admin.site.register(ExamsResult, ExamsResultAdmin)


class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'registration_date')
    search_fields = ('student__registration_no', 'course__course_name')
    list_filter = ('semester', 'year')

admin.site.register(CourseRegistration, CourseRegistrationAdmin)
