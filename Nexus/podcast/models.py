from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when the object is created

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
