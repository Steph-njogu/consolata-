from django.contrib import admin
from .models import User

#admin for the users display
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'first_name']
    search_fields = ['first_name', 'username']
    prepopulated_fields = {'slug': ('username',)}
admin.site.register(User, UserAdmin)


