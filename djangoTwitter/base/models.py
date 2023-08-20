from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tweet = models.TextField(max_length=140, blank=False, null=False)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tweet
    
    class Meta:
        ordering = ['-created']