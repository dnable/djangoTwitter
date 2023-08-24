from django.contrib import admin

# Register your models here.
from .models import Tweet, Follower

admin.site.register(Tweet)
admin.site.register(Follower)