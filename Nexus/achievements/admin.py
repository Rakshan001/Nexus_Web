# achievements/admin.py
from django.contrib import admin
from .models import Achievement

class AchievementAdmin(admin.ModelAdmin):
    autocomplete_fields = ['alumni']  # Enables searchable dropdown for alumni
    list_display = ['title', 'alumni', 'date_achieved', 'category']

admin.site.register(Achievement, AchievementAdmin)
    