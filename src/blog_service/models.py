from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    name = models.CharField(max_length=140)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=False)
    text = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    subscriber = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='subscriptions'
                                    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog


class PostRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
