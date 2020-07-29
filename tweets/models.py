from django.db import models
import random
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add= True)




class Tweet(models.Model):
    parent = models.ForeignKey("self", null = True, on_delete = models.SET_NULL)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    content = models.TextField(blank=True, null =True)
    likes = models.ManyToManyField(User, related_name= 'tweet_user', blank = True, through= TweetLike)
    image   = models.FileField(upload_to = 'images/', blank= True, null=True)
    timestamp = models.DateTimeField(auto_now_add= True)

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