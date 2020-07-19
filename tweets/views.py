from django.shortcuts import render, redirect
from .models import Tweet
from django.http import HttpResponse, Http404, JsonResponse
import random
from django.utils.http import is_safe_url
from .forms import TweetForm
from django.conf import settings


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
    tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0,12332) } for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit = False)
        obj.save()
        if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context= {"form": form})