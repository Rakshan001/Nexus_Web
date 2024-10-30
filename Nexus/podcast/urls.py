# podcast/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('videos/', views.video_list, name='video_list'),
]
