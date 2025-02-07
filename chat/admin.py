from django.contrib import admin
from .models import Thread, Reply

# Inline model to display threads inside the Category admin view
class ThreadInline(admin.TabularInline):
    model = Thread
    extra = 1  # Number of empty forms to display by default


# Register Thread model
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('slug',  'author', 'image', 'vedio', 'document', 'created_at', 'updated_at')  # Display relevant columns
    search_fields = ('author__username',)  # Search by title, category name, an
  
    

# Register Reply model
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')  # Columns to display in list view
    search_fields = ('content', 'author__username')  # Search by content, author, and thread title
    list_filter = ('thread', 'author')  # Filter by thread and author

