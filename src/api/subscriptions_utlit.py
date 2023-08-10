from django.core.cache import cache
from rest_framework.response import Response

def get_cache_key(user_id, blog_id):
    return f'subscribe:{user_id}:{blog_id}'


def check_cache_and_return_response(cache_key, message, status_code):
    cached_result = cache.get(cache_key)
    if cached_result:
        return Response({'message': message}, status=status_code)
    return None


def set_cache(cache_key, value):
    cache.set(cache_key, value, 3600)  # Save result in cache for an hour


def perform_subscription(user, blog_id):
    new_subscription = Subscription.objects.create(
        subscriber=user,
        blog_id=blog_id)
    return new_subscription


def delete_subscription(existing_subscription):
    existing_subscription.delete()
