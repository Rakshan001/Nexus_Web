# notifications/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from events_cec.models import Event
from django.contrib.auth.models import User
from .models import Notification
from datetime import timedelta
from django.utils import timezone

@receiver(post_save, sender=Event)
def create_event_notification(sender, instance, created, **kwargs):
    if created:  # Only when a new event is created
        # Create notification for all users
        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                recipient=user,
                notification_type='upcoming_event',
                title=f"New Event: {instance.title}",
                message=f"A new event '{instance.title}' has been scheduled for {instance.date}",
                related_event=instance
            )

# You might also want to create a periodic task to notify about upcoming events
def notify_upcoming_events():
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming_events = Event.objects.filter(date=tomorrow)
    
    for event in upcoming_events:
        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                recipient=user,
                notification_type='upcoming_event',
                title=f"Reminder: {event.title} tomorrow",
                message=f"Don't forget! The event '{event.title}' is happening tomorrow!",
                related_event=event
            )