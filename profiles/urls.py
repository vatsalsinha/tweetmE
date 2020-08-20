from django.urls import path, include
from .views import profile_detail_view, profile_update_view

urlpatterns = [
    path('<str:username>/', profile_detail_view),
    path('edit', profile_update_view),
]