'''
from django.db import models

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)

    def __str__(self):
        return self.event_title


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_images', default=None)
    image = models.ImageField(upload_to='event_images/')

    def __str__(self):
        return f"Image for {self.event.event_title}"
'''


# from django.db import models
# from django.core.exceptions import ValidationError

# def validate_image_size(image):
#     max_size = 2 * 1024 * 1024  # 2 MB limit
#     if image.size > max_size:
#         raise ValidationError('Image file too large ( > 2mb )')

# class Event(models.Model):
#     event_id = models.AutoField(primary_key=True)
#     event_title = models.CharField(max_length=200)
#     description = models.TextField()
#     date = models.DateField()
#     location = models.CharField(max_length=200)
#     poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)

#     def __str__(self):
#         return self.event_title


# class EventImage(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_images', default=None)
#     image = models.ImageField(upload_to='event_images/', validators=[validate_image_size])

#     def __str__(self):
#         return f"Image for {self.event.event_title}"

from django.db import models
from django.core.exceptions import ValidationError
import os
from datetime import datetime

def validate_image_size(image):
    max_size = 2 * 1024 * 1024  # 2 MB limit
    if image.size > max_size:
        raise ValidationError('Image file too large ( > 2mb )')

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)  # New time field
    location = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)

    def __str__(self):
        return self.event_title


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_images', default=None)
    image = models.ImageField(upload_to='event_images/', validators=[validate_image_size])

    def __str__(self):
        return f"Image for {self.event.event_title}"

    def save(self, *args, **kwargs):
        # Check if this is an update (not a new instance)
        if self.pk is not None:
            # Get the current instance from the database
            current_instance = EventImage.objects.get(pk=self.pk)
            # If the image field has changed, delete the old image
            if current_instance.image != self.image:
                if current_instance.image:
                    # Delete the old image file from the filesystem
                    if os.path.isfile(current_instance.image.path):
                        os.remove(current_instance.image.path)

        super().save(*args, **kwargs)

    
