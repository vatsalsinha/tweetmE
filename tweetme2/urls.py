"""tweetme2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tweets import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.tweets_list_view),
    path('api/tweets/', include('tweets.api.urls')),
    path('<int:tweet_id>', views.tweets_detail_view),
    path('profile/<str:username', views.tweets_profile_view)
    #path('tweets/<int:tweet_id>', views.tweet_detail_view),
    #path('tweets', views.tweet_list_view),
    #path('api/tweets', views.tweet_list_view),
    #path('create-tweet', views.tweet_create_view),
    #path('api/tweets/<int:tweet_id>/delete', views.tweet_delete_view),
    #path('api/tweets/action', views.tweet_action_view)
    #path('react/', TemplateView.as_view(template_name = 'react_via_django.html'))
]

if settings.DEBUG:
    urlpatterns +=  static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)