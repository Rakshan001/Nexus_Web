from django.urls import path
from .views import FacultyCoordinatorListView, StudentCoordinatorListView

urlpatterns = [
    path('faculty-coordinators/', FacultyCoordinatorListView.as_view(), name='faculty-coordinator-list'),
    path('student-coordinators/', StudentCoordinatorListView.as_view(), name='student-coordinator-list'),
]
