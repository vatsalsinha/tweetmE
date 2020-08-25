from rest_framework import serializers
from .models import Profile

from django.conf import settings

class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only = True)
    last_name = serializers.SerializerMethodField(read_only = True)
    username = serializers.SerializerMethodField(read_only = True)
    followers_count = serializers.SerializerMethodField(read_only = True)
    following_count = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'id' ,'location', 'bio', 'followers_count', 'following_count', 'username'
        ]

    def get_first_name(self, obj):
        return obj.user.first_name
    def get_last_name(self, obj):
        return obj.user.last_name
    def get_username(self, obj):
        return obj.user.username
    def get_followers_count(self, obj):
        return obj.followers.count()
    def get_following_count(self, obj):
        return obj.user.following.count()