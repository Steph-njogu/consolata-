from django.contrib import admin
from .models import Event, Diary, Calendar

# Customizing the admin for Event model
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'color', 'created_at')
    search_fields = ('title', 'description', 'location')
    list_filter = ('event_date', 'color')
    prepopulated_fields = {'slug': ('title',)}  # Automatically create slug from title

# Customizing the admin for Diary model
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # Automatically create slug from name

# Customizing the admin for Calendar model
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('event', 'highlight_date', 'note')
    list_filter = ('highlight_date',)
    search_fields = ('event__title',)  # Search by event title

# Customizing the admin for Registration model

# Register your models here
admin.site.register(Event, EventAdmin)
admin.site.register(Diary, DiaryAdmin)
admin.site.register(Calendar, CalendarAdmin)
