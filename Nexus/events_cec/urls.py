from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the event list page
    path('events/', views.event_list, name='event_list'),
    
    # URL pattern for the event detail page
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
]