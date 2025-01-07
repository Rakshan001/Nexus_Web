from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Notification
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from utils.decorators import login_required_with_message

@login_required_with_message
def notification_panel(request):
    # Get notifications from the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    notifications_list = Notification.objects.filter(
        recipient=request.user,
        created_at__gte=thirty_days_ago
    ).order_by('-created_at')

    # Pagination
    paginator = Paginator(notifications_list, 10)  # Show 10 notifications per page
    page = request.GET.get('page', 1)
    notifications = paginator.get_page(page)
    
    unread_count = notifications_list.filter(viewed=False).count()

    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/notification_panel.html', context)

@login_required_with_message
@csrf_protect
def mark_as_read(request, notification_id):
    if request.method == 'POST':
        try:
            notification = Notification.objects.get(
                id=notification_id, 
                recipient=request.user
            )
            notification.viewed = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)

@login_required_with_message
@csrf_protect
def mark_all_as_read(request):
    if request.method == 'POST':
        Notification.objects.filter(
            recipient=request.user, 
            viewed=False
        ).update(viewed=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required_with_message
def get_unread_count(request):
    count = Notification.objects.filter(
        recipient=request.user, 
        viewed=False
    ).count()
    return JsonResponse({'count': count})