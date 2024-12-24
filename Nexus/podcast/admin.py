# podcast/admin.py

from django.contrib import admin
from .models import Podcast

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_url','uploaded_at')
