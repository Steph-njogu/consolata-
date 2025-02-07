from django.contrib import admin
from .models import AdmissionStaff, AdmissionStudent

# Register your models here.
class AdmissionStudentAdmin(admin.ModelAdmin):
    list_display = ['registration_no', 'slug', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['registration_no']
    prepopulated_fields = {'slug': ('registration_no',)}

class AdmissionStaffAdmin(admin.ModelAdmin):
    list_display = ['staff_no', 'slug', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['staff_no']
    prepopulated_fields = {'slug': ('staff_no',)}


admin.site.register(AdmissionStaff, AdmissionStaffAdmin)
admin.site.register(AdmissionStudent, AdmissionStudentAdmin)
