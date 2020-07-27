from rest_framework import serializers
from .models import Tweet

from django.conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip() 
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("this is not a valid action for tweets")
        return value
class TweetSerializer(serializers.ModelSerializer):     
    likes = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']

    def get_likes(self,obj):
        return obj.likes.count()
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("Tweet too long")
        return value