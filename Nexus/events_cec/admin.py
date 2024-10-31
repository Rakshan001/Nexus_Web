
'''
# This is normal admin it doesnot show any preview 

from django.contrib import admin
from .models import Event, EventImage

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1
    fields = ['image'] 

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'date', 'location')
    search_fields = ('event_title', 'location')
    list_filter = ('date',)
    ordering = ('-date',)
    inlines = [EventImageInline]
'''




# This pannel use libarary for preview comment below code and use above code

from django.contrib import admin
from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import Event, EventImage

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1
    fields = ['image']  # Fields to display for inline images
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},  # Use the custom widget for image uploads
    }

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'date', 'location')
    search_fields = ('event_title', 'location')
    list_filter = ('date',)
    ordering = ('-date',)
    inlines = [EventImageInline]
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},  # Use the custom widget for the event poster
    }
