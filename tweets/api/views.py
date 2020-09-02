from django.shortcuts import render, redirect
from ..models import Tweet
from django.http import HttpResponse, Http404, JsonResponse
import random
from django.utils.http import is_safe_url
from ..forms import TweetForm
from django.conf import settings
from ..serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = TweetSerializer(paginated_qs, many=True, context = {"request": request}) # agar tweet ke andar bhi daalna hai is_following, to context variable yaha daalna hoga jaisa profiles->api->views me kiya tha
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status = 201)
    return Response({}, status = 400) 

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')
    if username != None:
        qs = qs.by_username(username)
    serializer = TweetSerializer(qs, many=True)
    return get_paginated_queryset_response(qs, request)
    
@api_view(['GET'])
def tweet_detail_view(request, tweet_id,  *args, **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status = 404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status = 200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status = 404)
    qs = qs.filter(user = request.user)
    if not qs.exists():
        return Response({"message": "You aren't authorised to delete this tweet"}, status = 401 )
    obj = qs.first()
    obj.delete()
    return Response({"message": "You have successfully deleted your tweet"}, status = 200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception= True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id = tweet_id)
        if not qs.exists():
            return Response({}, status = 404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status = 200)
        elif action == "unlike":
            obj.likes.remove(request.user)      
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status = 200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(user = request.user, parent = obj, content = content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status = 201)
        
    return Response({}, status = 200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request, *args, **kwargs):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    user = request.user
    qs = Tweet.objects.feed(user)
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = TweetSerializer(paginated_qs, many=True)
    return get_paginated_queryset_response(qs, request)




