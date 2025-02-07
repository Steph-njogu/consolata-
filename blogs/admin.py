from django.contrib import admin
from .models import Category, NewsArticle, Subscriber
from django.utils.html import format_html

# Register Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# Register NewsArticle model
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'category', 'date_added']
    search_fields = ['title', 'author']

# Register Subscriber model with custom actions
def delete_selected(modeladmin, request, queryset):
    queryset.delete()

delete_selected.short_description = "Delete selected subscribers"

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'active']
    search_fields = ['email']

    # Adding custom actions
    actions = [delete_selected]



# Register models to the admin site
admin.site.register(Category, CategoryAdmin)
admin.site.register(NewsArticle, NewsArticleAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
