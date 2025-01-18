# podcast/views.py

from django.shortcuts import render
from .models import Podcast
from django.conf import settings

def podcast(request):
    podcasts = Podcast.objects.all()
    context = {
        'podcasts': podcasts,
        'debug': settings.DEBUG  # This will show debug info only in development
    }
    return render(request, 'podcast/video.html', context)


