from django.contrib import admin
from .models import AdmissionStaff, AdmissionStudent
from django.core.exceptions import PermissionDenied

# Register your models here.
class AdmissionStudentAdmin(admin.ModelAdmin):
    list_display = ['registration_no', 'slug', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['registration_no']
    prepopulated_fields = {'slug': ('user',)}
    actions = ['verify_student']


    def verify_student(self, request, queryset):
        """Admin action to verify students."""
        if not request.user.is_superuser:
            raise PermissionDenied("You must be an admin to verify students.")
        
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} student(s) verified successfully.")

    verify_student.short_description = "Verify selected students"

    

class AdmissionStaffAdmin(admin.ModelAdmin):
    list_display = ['staff_no', 'slug', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['staff_no']
    prepopulated_fields = {'slug': ('user',)}
    actions = ['verify_staff']


    def verify_staff(self, request, queryset):
        """Admin action to verify staff members."""
        if not request.user.is_superuser:
            raise PermissionDenied("You must be an admin to verify staff.")
        
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} staff member(s) verified successfully.")

    verify_staff.short_description = "Verify selected staff members"


admin.site.register(AdmissionStaff, AdmissionStaffAdmin)
admin.site.register(AdmissionStudent, AdmissionStudentAdmin)
