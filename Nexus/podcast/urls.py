# podcast/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('videos/', views.podcast, name='podcast'),
]
