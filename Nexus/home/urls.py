from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page (publicly accessible)
    path('', views.home, name='home'),

    # User login and logout views
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    # Alumni-specific profile view (requires login and alumni status)
    path('alumni/profile/', views.alumni_profile, name='alumni_profile'),

    
# '''This is the Forgot password setup'''

    
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='home/registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='home/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='home/registration/password_reset_complete.html'), name='password_reset_complete'),
    path('nexusTeam/', views.nexusTeam, name='nexusTeam'),
    path('webTeam/', views.webTeam, name='webTeam'),
]


