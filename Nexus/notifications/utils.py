from django.urls import reverse
from .models import Notification
from events_cec.models import Event
from alumni_details.models import Alumni, Student
from django.utils import timezone

def create_profile_view_notification(viewer, profile_owner):
    """
    Create a notification when someone views a profile
    """
    if viewer != profile_owner:
        viewer_type = None
        viewer_name = None
        viewer_photo = None
        viewer_profile_url = None
        notification_type = None

        # Determine if viewer is a student or alumni
        try:
            if hasattr(viewer, 'student_profile'):
                student = viewer.student_profile
                viewer_type = 'student'
                viewer_name = f"{student.first_name} {student.last_name}"
                notification_type = 'profile_view_student'
                # You might want to add a default student photo
                viewer_photo = '/static/images/default_student.png'
                
            elif hasattr(viewer, 'alumni_profile'):
                alumni = viewer.alumni_profile
                viewer_type = 'alumni'
                viewer_name = f"{alumni.first_name} {alumni.last_name}"
                notification_type = 'profile_view_alumni'
                viewer_photo = alumni.profile_picture.url if alumni.profile_picture else '/static/images/default_alumni.png'
                viewer_profile_url = reverse('public_alumni_profile', kwargs={'alumni_id': alumni.alumni_id})

        except Exception as e:
            print(f"Error determining viewer type: {e}")
            return

        # Create the notification with appropriate message
        message = (
            f"{viewer_name} ({viewer_type.title()}) viewed your profile"
            if viewer_type == 'student'
            else f"{viewer_name} (Alumni) viewed your profile. Click to view their profile."
        )

        Notification.objects.create(
            recipient=profile_owner,
            notification_type=notification_type,
            title='Profile View',
            message=message,
            viewer_name=viewer_name,
            viewer_photo=viewer_photo,
            viewer_profile_url=viewer_profile_url,
            viewer_type=viewer_type
        )

def create_upcoming_event_notification(event, user):
    """
    Create a notification for upcoming events
    """
    Notification.objects.create(
        recipient=user,
        notification_type='upcoming_event',
        title='Upcoming Event',
        message=f'New event: {event.event_title} on {event.date}',
        related_event=event
    )

# notifications/utils.py
from django.utils import timezone
from datetime import timedelta
from .models import Notification

def delete_old_notifications():
    """Delete notifications older than 100 days"""
    cutoff_date = timezone.now() - timedelta(days=100)
    deleted_count, _ = Notification.objects.filter(created_at__lt=cutoff_date).delete()
    return deleted_count