from django.contrib import admin
from . models import Index

class IndexAdmin(admin.ModelAdmin):
    list_display = ['content']

admin.site.register(Index, IndexAdmin)