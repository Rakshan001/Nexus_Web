from django.db import models
from django.contrib.auth.models import User
from alumni_details.models import Alumni,Student

class Podcast(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField(max_length=500)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when the object is created
    hosts = models.ManyToManyField(Student, related_name="hosted_podcasts", blank=True)
    speakers = models.ManyToManyField(Alumni, related_name="spoken_podcasts", blank=True)

    def __str__(self):
        return self.title

    def embed_url(self):
        """
        Convert the standard YouTube URL into an embeddable URL.
        Supports both 'youtu.be' and 'youtube.com' formats.
        """
        if 'youtu.be' in self.youtube_url:
            return self.youtube_url.replace('youtu.be/', 'youtube.com/embed/')
        elif 'watch?v=' in self.youtube_url:
            return self.youtube_url.replace('watch?v=', 'embed/')
        return self.youtube_url  # In case it's already in embed format