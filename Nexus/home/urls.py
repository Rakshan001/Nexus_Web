from django.urls import path
from . import views

urlpatterns = [
    # Home page (publicly accessible)
    path('', views.home, name='home'),

    # User login and logout views
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    # Alumni-specific profile view (requires login and alumni status)
    path('alumni/profile/', views.alumni_profile, name='alumni_profile'),
]
