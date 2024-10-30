from django.contrib import admin
from .models import FacultyCoordinator, StudentCoordinator

# Faculty Coordinator Admin
@admin.register(FacultyCoordinator)
class FacultyCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('coordinator_id', 'name', 'department', 'email', 'phone_number')  # Columns to display
    search_fields = ('name', 'department', 'email')  # Fields to search by

# Student Coordinator Admin
@admin.register(StudentCoordinator)
class StudentCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('coordinator_id', 'name', 'branch', 'email', 'phone_number')  # Columns to display
    search_fields = ('name', 'branch', 'email')  # Fields to search by
