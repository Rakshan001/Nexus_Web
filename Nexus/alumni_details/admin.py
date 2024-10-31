from django.contrib import admin
from django.db import models
from .models import Student, Alumni, CouncilMember
from image_uploader_widget.widgets import ImageUploaderWidget

class StudentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']  # Replaces dropdown with search box
    list_display = ['first_name', 'last_name', 'usn', 'batch']
    list_filter = ['batch']  # Adds filter by batch

class AlumniAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['first_name', 'last_name', 'usn', 'batch']
    search_fields = ['first_name', 'last_name', 'usn', 'batch', 'personal_email', 'company_name', 'current_position']  # Defines fields to search by
    list_filter = ['batch', 'graduation_year']  # Adds filter by batch and graduation year
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }

class CouncilMemberAdmin(admin.ModelAdmin):
    list_display = ('role', 'year', 'alumni')
    list_filter = ('role', 'year')
    search_fields = ('alumni__first_name', 'alumni__last_name', 'role')
    ordering = ('-year', 'role')  # Orders by year descending, then by role

    def alumni(self, obj):
        return f"{obj.alumni.first_name} {obj.alumni.last_name}"
    alumni.short_description = 'Alumni Name'

# Registering models with admin site
admin.site.register(Student, StudentAdmin)
admin.site.register(Alumni, AlumniAdmin)
admin.site.register(CouncilMember, CouncilMemberAdmin)  
