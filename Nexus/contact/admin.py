from django.contrib import admin
from .models import ContactForm

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'branch', 'subject', 'date_sent', 'is_read', 'is_important')
    list_filter = ('subject', 'is_read', 'is_important', 'date_sent')
    search_fields = ('name', 'email', 'branch', 'subject')
    actions = ['mark_as_read', 'mark_as_important']

    # Custom action to mark selected entries as read
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected entries as Read"

    # Custom action to mark selected entries as important
    def mark_as_important(self, request, queryset):
        queryset.update(is_important=True)
    mark_as_important.short_description = "Mark selected entries as Important"
