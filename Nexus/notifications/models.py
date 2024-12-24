from django.db import models
from django.contrib.auth.models import User
from alumni_details.models import Alumni, Student
from events_cec.models import Event
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('profile_view_student', 'Profile View by Student'),
        ('profile_view_alumni', 'Profile View by Alumni'),
        ('upcoming_event', 'Upcoming Event'),
        ('system', 'System Notification'),
        ('targeted', 'Targeted Notification'), 
         ('contribution', 'Contribution Notification'),  # New type for targeted messages
    ]

    TARGET_GROUPS = [
        ('all', 'All Users'),
        ('students', 'Students Only'),
        ('alumni', 'Alumni Only'),
        ('specific', 'Specific Users')
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=25, choices=NOTIFICATION_TYPES)
    target_group = models.CharField(max_length=20, choices=TARGET_GROUPS, default='all')
    title = models.CharField(max_length=255)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Viewer details
    viewer_name = models.CharField(max_length=255, null=True, blank=True)
    viewer_photo = models.URLField(max_length=1000, null=True, blank=True)
    viewer_profile_url = models.CharField(max_length=500, null=True, blank=True)
    viewer_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('alumni', 'Alumni')], null=True)
    
    # Related models
    related_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} - {self.title}"
    
    @classmethod
    def delete_old_notifications(cls):
        cutoff_date = timezone.now() - timedelta(days=100)
        cls.objects.filter(created_at__lt=cutoff_date).delete()

# Signal to trigger cleanup whenever a new notification is created
@receiver(post_save, sender=Notification)
def cleanup_old_notifications(sender, **kwargs):
    Notification.delete_old_notifications()