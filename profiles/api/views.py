from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
import random
from django.utils.http import is_safe_url
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from ..models import Profile
from django.contrib.auth import get_user_model
from ..serializers import PublicProfileSerializer

User = get_user_model()
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# @api_view(['GET'])
# #@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def user_profile_detail_view(request, username, *args, **kwargs):
#     current_user = request.user
#     to_follow_user = 
#     return Response({}, status = 200) 
@api_view(['GET'])
def profile_detail_api_view(request, username, *args, **kwargs):
    # get the profile for the passed username
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User not found"}, status = 404)
    profile_obj = qs.first()
    data = PublicProfileSerializer(instance = profile_obj, context = {"request": request}) #we can send data to a serializer like done here through 'context'
    return Response(data.data, status = 200) 

@api_view(['GET', 'POST'])
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_follow_view(request, username, *args, **kwargs):
    me = request.user
    other_user_qs = User.objects.filter(username = username)
    if me.username == username:
        my_followers = me.profile.followers.all()
        return Response({"count": my_followers.count()}, status = 200) 
    if not other_user_qs.exists():
        return Response({}, status = 404)
    other = other_user_qs.first()
    profile = other.profile
    data = request.data or {}
    print(data)
    action = data.get("action")
    if action == "follow":
        profile.followers.add(me)
    elif action == "unfollow":
        profile.followers.remove(me)
    else:
        pass
    data = PublicProfileSerializer(instance = profile, context = {"request": request})
    return Response(data.data, status = 200) 

