from django.urls import path
from . import views

# ENDPOINT = /api/profiles/

urlpatterns = [
    path('<str:username>/follow', views.profile_detail_api_view),
    path('<str:username>/', views.profile_detail_api_view) 
]