from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Blog


@receiver(post_save, sender=User)
def create_personal_blog(sender, instance, created, **kwargs):
    """Создает персональный блог при регистрации нового пользователя."""
    if created:
        Blog.objects.create(name=f"{instance.username}'s Blog", user=instance)
