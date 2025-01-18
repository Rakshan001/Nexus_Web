
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
from .models import Event, EventImage, Gallery

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



@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_uploaded')  # Fields to display in the admin list view
    search_fields = ('title',)  # Search functionality by title
    list_filter = ('date_uploaded',)  # Filter by date uploaded
    ordering = ('-date_uploaded',)  # Order by most recent uploads
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},  # Use the custom widget for image uploads
    }



# Admin configurations to handle uploading from the admin panel
from django.contrib import admin
from .models import SocialMediaReels,SocialMediaPosts,SocialMediaImages



# Social Media Reels Admin
from django.utils.text import Truncator
class SocialMediaReelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'shortened_url', 'date_uploaded']
    
    def shortened_url(self, obj):
        # Use Truncator to truncate the URL to a specified length
        return Truncator(obj.url).chars(30)  # Adjust 30 to the length you want
    shortened_url.short_description = 'URL'  # Set the column name in admin
    
    def has_add_permission(self, request):
        # Limit the number of reels to 4
        if SocialMediaReels.objects.count() >= 4:
            return False
        return super().has_add_permission(request)

# Social Media Posts Admin
class SocialMediaPostsAdmin(admin.ModelAdmin):
    list_display = ['description', 'url', 'date_uploaded']
    
    def has_add_permission(self, request):
        # Limit the number of posts to 4
        if SocialMediaPosts.objects.count() >= 4:
            return False
        return super().has_add_permission(request)
    
    # Set custom widget to enable image preview in admin panel
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},  # Use the ImageUploaderWidget for image fields
    }

# Social Media Images Admin
class SocialMediaImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'images', 'date_uploaded']
    
    def has_add_permission(self, request):
        # Limit the number of images to 4
        if SocialMediaImages.objects.count() >= 8:
            return False
        return super().has_add_permission(request)
    
    # Set custom widget to enable image preview in admin panel
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},  # Use the ImageUploaderWidget for image fields
    }



from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import ActivityCount

class ActivityCountAdmin(admin.ModelAdmin):
    list_display = ['podcast', 'events', 'workshops', 'interactions']

    # Restrict adding more than one record
    def save_model(self, request, obj, form, change):
        # Check if this is a new record and there is already an existing record
        if not obj.pk and ActivityCount.objects.exists():
            raise ValidationError("Only one record is allowed in ActivityCount.")
        super().save_model(request, obj, form, change)

    # Disable the 'Add ActivityCount' button if one record already exists
    def has_add_permission(self, request):
        if ActivityCount.objects.exists():
            return False
        return True

# Register the model with the custom admin
admin.site.register(ActivityCount, ActivityCountAdmin)




# Register models with admin site
admin.site.register(SocialMediaReels, SocialMediaReelsAdmin)
admin.site.register(SocialMediaPosts, SocialMediaPostsAdmin)
admin.site.register(SocialMediaImages, SocialMediaImagesAdmin)
