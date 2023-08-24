from django.contrib import admin
from .models import Tweet, Follower


class TweetAdmin(admin.ModelAdmin):
    list_display = ("user", "tweet", "created",)


class FollowerAdmin(admin.ModelAdmin):
    list_display = ("user","follower","when",)



admin.site.register(Tweet, TweetAdmin)
admin.site.register(Follower, FollowerAdmin)