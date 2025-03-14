# admin.py
from django.contrib import admin
from .models import Author, Publisher, EBook, LibraryUser, EBookLoan, Category, EBookHistory, EBookDownload,Note,Department
@admin.register(EBook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ['category', 'author', 'title', 'isbn', 'genre']
    search_fields = ['author', 'title', 'category']
    
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['course', 'lecturer', 'slug', 'updated', 'yearOfStudy', 'department', 'file', 'approved']
    list_filter = ['approved']
    prepopulated_fields = {'slug': ('course',)}
    list_editable = ['file', 'yearOfStudy']

admin.site.register(Department)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(LibraryUser)
admin.site.register(Category)
admin.site.register(EBookHistory)
admin.site.register(EBookDownload)
admin.site.register(EBookLoan)