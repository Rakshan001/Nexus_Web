# podcast/admin.py

from django.contrib import admin
from .models import Podcast

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_url','uploaded_at')
    filter_horizontal = ('hosts', 'speakers')
    search_fields = ['title', 'description']
    list_filter = ['uploaded_at']
    ordering = ['-uploaded_at']
    readonly_fields = ['uploaded_at']

