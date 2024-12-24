# urls.py
from django.urls import path
# from .views import alumni_profile, update_alumni_profile
from . import views

urlpatterns = [
    path('alumni/profile/', views.alumni_profile, name='alumni_profile'),
    path('alumni/update/', views.update_alumni_profile, name='update_alumni_profile'),
     path('delete-profile-picture/', views.delete_profile_picture, name='delete_profile_picture'),

    # *******************
      path('alumni-details/', views.alumni_list, name='alumni_list'),  # Main alumni list view
    path('alumni/<int:graduation_year>/', views.alumni_by_year, name='alumni_by_year'),
# load more years
    path('load-more/', views.load_more_years, name='load_more_years'),
    
    #single Alumni profile

path('alumni-profile/<uuid:uuid>/', views.public_alumni_profile, name='public_alumni_profile'),
path('share-alumni-profile/', views.share_alumni_profile, name='share_alumni_profile'),

    



#====================
    path('manage_memories/', views.manage_memories, name='manage_memories'),
    # path('delete-memory/<int:memory_id>/', views.delete_memory, name='delete_memory'),



    # **********************
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('alumni-search/', views.alumni_search, name='alumni_search'),

    # search result
    # path('alumni/search/', views.search_alumni, name='search_alumni'),


     path('council_members/', views.council_members_view, name='council_members'),
]

