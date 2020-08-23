from django.db import models
import random
from django.conf import settings
from django.db.models import Q
User = settings.AUTH_USER_MODEL

# Create your models here.

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add= True)


class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact = username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat = True)
        return self.filter(
            Q(user__id__in = followed_users_id) |
            Q(user = user)
        ).distinct().order_by("-timestamp")    

class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using= self._db)
    def feed(self,user):
        return self.get_queryset().feed(user)

class Tweet(models.Model):
    parent = models.ForeignKey("self", null = True, on_delete = models.SET_NULL)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="tweets")
    content = models.TextField(blank=True, null =True)
    likes = models.ManyToManyField(User, related_name= 'tweet_user', blank = True, through= TweetLike)
    image   = models.FileField(upload_to = 'images/', blank= True, null=True)
    timestamp = models.DateTimeField(auto_now_add= True)
    objects = TweetManager()

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,200)
        }

    @property
    def is_retweet(self):
        return self.parent != None
    

    def __str__(self):
        if not self.content:
            return ""
        return self.content