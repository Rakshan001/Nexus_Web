from django.shortcuts import render
from django.views.generic import ListView
from .models import FacultyCoordinator, StudentCoordinator

# List View for Faculty Coordinators
class FacultyCoordinatorListView(ListView):
    model = FacultyCoordinator
    template_name = 'coordinators/faculty-coordinators.html'  # HTML template to render
    context_object_name = 'faculty_coordinators'  # Name of the object in the template

# List View for Student Coordinators
class StudentCoordinatorListView(ListView):
    model = StudentCoordinator
    template_name = 'coordinators/student-coordinators.html'  # HTML template to render
    context_object_name = 'student_coordinators'  # Name of the object in the template
