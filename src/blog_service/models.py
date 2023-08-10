from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    subscriber = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='subscriptions'
                                    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)