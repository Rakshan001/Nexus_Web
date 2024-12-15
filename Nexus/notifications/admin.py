# notifications/admin.py
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from alumni_details.models import Alumni, Student
from .models import Notification
from .forms import CustomNotificationForm

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'recipient', 'created_at', 'viewed']
    list_filter = ['notification_type', 'viewed', 'created_at']
    search_fields = ['title', 'message', 'recipient__username']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('send-bulk/', self.send_bulk_view, name='notifications_notification_send_bulk'),
        ]
        return my_urls + urls

    def send_bulk_view(self, request):
        if request.method == 'POST':
            form = CustomNotificationForm(request.POST)
            if form.is_valid():
                recipient_type = form.cleaned_data['recipient_type']
                title = form.cleaned_data['title']
                message = form.cleaned_data['message']
                
                # Get users based on recipient type
                users = []
                if recipient_type == 'all':
                    users = User.objects.all()
                elif recipient_type == 'alumni':
                    # Get users who have alumni profiles
                    alumni_users = Alumni.objects.all().values_list('user', flat=True)
                    users = User.objects.filter(id__in=alumni_users)
                elif recipient_type == 'students':
                    # Get users who have student profiles
                    student_users = Student.objects.all().values_list('user', flat=True)
                    users = User.objects.filter(id__in=student_users)
                elif recipient_type == 'specific':
                    users = form.cleaned_data['specific_users']

                if users:
                    # Create notifications
                    for user in users:
                        Notification.objects.create(
                            recipient=user,
                            notification_type='targeted',
                            target_group=recipient_type,
                            title=title,
                            message=message
                        )
                    self.message_user(request, f'Successfully sent notifications to {len(users)} users.')
                    return HttpResponseRedirect("../")
                else:
                    messages.warning(request, "No users found for the selected recipient type.")
        else:
            form = CustomNotificationForm()

        return render(
            request,
            'admin/notifications/custom_notification_form.html',
            {'form': form, 'title': 'Send Bulk Notification'}
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_bulk_notification_button'] = True
        return super().changelist_view(request, extra_context=extra_context)