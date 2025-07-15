from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    path('manage/', views.user_and_franchise_management, name='user_and_franchise_management'),
]
