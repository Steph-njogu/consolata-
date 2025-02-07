from django.contrib import admin
from . models import Timetable

# Register your models here.

class TimetableAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'image', 'document', 'slug', 'date_added']
    search_fields = ['title',]
    list_filter = ['title']
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Timetable, TimetableAdmin)