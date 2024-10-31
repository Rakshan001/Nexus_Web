from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_form, name='submit_form'),
    path('form-success/', views.form_success, name='form_success'),

]
