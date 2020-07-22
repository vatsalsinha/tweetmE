from django.shortcuts import render, redirect
from .models import Tweet
from django.http import HttpResponse, Http404, JsonResponse
import random
from django.utils.http import is_safe_url
from .forms import TweetForm
from django.conf import settings
from .serializers import TweetSerializer


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context = {}, status = 200)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id
    }
    status = 200
    try:
        obj = Tweet.objects.get(id = tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
   
    return JsonResponse(data, status = status )

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user 
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status = 401 )
        return redirect(settings.LOGIN_URL) 
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data = request.POST or None)
    if serializer.is_valid():
        obj = serializer.save(user = request.user)
        return JsonResponse(serializer.data, status = 201)
    return JsonResponse({}, status = 400)