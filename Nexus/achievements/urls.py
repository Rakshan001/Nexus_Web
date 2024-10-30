# achievements/urls.py

from django.urls import path
from .views import achievements_list ,alumni_profile

urlpatterns = [
    path('', achievements_list, name='achievements_list'),
     path('profile/<int:alumni_id>/', alumni_profile, name='alumni_profile'),
]
