from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_panel, name='notification_panel'),
    path('mark-read/<int:notification_id>/', views.mark_as_read, name='mark_notification_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_notifications_read'),
    path('get-unread-count/', views.get_unread_count, name='get_unread_count'),
]