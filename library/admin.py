# admin.py
from django.contrib import admin
from .models import Author, Publisher, EBook, LibraryUser, EBookLoan, Category, EBookHistory, EBookDownload, BookRecommendation

@admin.register(EBook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ['category', 'author', 'title', 'isbn', 'genre']
    search_fields = ['author', 'title', 'category']
    


admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(LibraryUser)

admin.site.register(Category)
admin.site.register(EBookHistory)
admin.site.register(EBookDownload)
admin.site.register(BookRecommendation)

admin.site.register(EBookLoan)

