# podcast/views.py

from django.shortcuts import render
from .models import Video

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'podcast/video.html', {'videos': videos})
