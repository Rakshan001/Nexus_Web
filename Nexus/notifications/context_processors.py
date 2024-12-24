from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            recipient=request.user, 
            viewed=False
        ).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}