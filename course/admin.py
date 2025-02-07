from django.contrib import admin
from .models import University, Campus, Department, YearOfStudy, Semester, Field, Course

# Registering University Model
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

admin.site.register(University, UniversityAdmin)


# Registering Campus Model
class CampusAdmin(admin.ModelAdmin):
    list_display = ('university', 'campus', 'description', 'slug')
    search_fields = ('university__name', 'campus')

admin.site.register(Campus, CampusAdmin)


# Registering Department Model
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('university', 'department_name', 'description', 'slug')
    search_fields = ('department_name',)

admin.site.register(Department, DepartmentAdmin)


# Registering YearOfStudy Model
class YearOfStudyAdmin(admin.ModelAdmin):
    list_display = ('department', 'year', 'slug')
    search_fields = ('department__department_name', 'year')

admin.site.register(YearOfStudy, YearOfStudyAdmin)


# Registering Semester Model
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('year', 'semester', 'slug')
    search_fields = ('year__department__department_name', 'semester')

admin.site.register(Semester, SemesterAdmin)


# Registering Field Model
class FieldAdmin(admin.ModelAdmin):
    list_display = ('semester', 'field_name', 'slug')
    search_fields = ('field_name',)

admin.site.register(Field, FieldAdmin)


# Registering Course Model
class CourseAdmin(admin.ModelAdmin):
    list_display = ('field', 'course_name', 'slug')
    search_fields = ('course_name',)

admin.site.register(Course, CourseAdmin)
