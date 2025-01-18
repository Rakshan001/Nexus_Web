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
    max_size = 5 * 1024 * 1024  # 2 MB limit
    if image.size > max_size:
        raise ValidationError('Image file too large ( > 2mb )')

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('workshop', 'Workshop'),
        ('talk', 'Alumni Talk'),
        ('others', 'Others'),
    ]
    event_id = models.AutoField(primary_key=True)
    event_title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)  # New time field
    location = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True,validators=[validate_image_size])
    instagram_url = models.URLField(max_length=500, blank=True, null=True)
    facebook_url = models.URLField(max_length=500, blank=True, null=True)
    youtube_url = models.URLField(max_length=500, blank=True, null=True)
    linkedin_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.event_title
    

    def delete(self, *args, **kwargs):
        # Delete image file from filesystem
        if self.poster and os.path.isfile(self.poster.path):
            os.remove(self.poster.path)
        super().delete(*args, **kwargs)


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


    def delete(self, *args, **kwargs):
        # Delete image file from filesystem
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    




class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=255)
    date= models.DateTimeField(blank=True,null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-date_uploaded']  # Order by most recent uploads first

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete image file from filesystem
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver

def validate_maximum_objects(model_class, limit):
    if model_class.objects.count() >= limit:
        raise ValidationError(f"Only {limit} items can be uploaded.")


# SocialMediaReels Model
class SocialMediaReels(models.Model):
    url = models.TextField(blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_uploaded']  # Order by most recent uploads first

    def save(self, *args, **kwargs):
        validate_maximum_objects(SocialMediaReels, 4)  # Pass model class explicitly
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url


class SocialMediaPosts(models.Model):
    url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='SocialMediaPosts/',validators=[validate_image_size])
    description = models.CharField(max_length=255)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_uploaded']  # Order by most recent uploads first

    def save(self, *args, **kwargs):
        validate_maximum_objects(SocialMediaPosts, 4)  # Pass model class explicitly
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description


class SocialMediaImages(models.Model):
    images = models.ImageField(upload_to='SocialMediaImages/',validators=[validate_image_size])
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_uploaded']  # Order by most recent uploads first

    def save(self, *args, **kwargs):
        validate_maximum_objects(SocialMediaImages, 8)  # Pass model class explicitly
        super().save(*args, **kwargs)

    def __str__(self):
        return self.images.name


# Signal to delete files from the media folder when the model instance is deleted
@receiver(post_delete, sender=SocialMediaPosts)
def delete_social_media_posts_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)

@receiver(post_delete, sender=SocialMediaImages)
def delete_social_media_images_file(sender, instance, **kwargs):
    if instance.images:
        instance.images.delete(save=False)


class ActivityCount(models.Model):
    podcast = models.IntegerField()
    events = models.IntegerField()
    workshops = models.IntegerField()
    interactions = models.IntegerField()

    def __str__(self):
        return f"Podcast: {self.podcast}, Events: {self.events}, Workshops: {self.workshops}, Interactions: {self.interactions}"
