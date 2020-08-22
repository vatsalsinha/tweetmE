from django.urls import path
from . import views

# ENDPOINT = /api/profiles/

urlpatterns = [
    path('<str:username>/follow', views.user_follow_view),
     
]