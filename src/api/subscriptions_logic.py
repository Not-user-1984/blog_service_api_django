from rest_framework import status
from rest_framework.response import Response
from api.subscriptions_utlit import (check_cache_and_return_response,
                                 delete_subscription, get_cache_key,
                                 perform_subscription, set_cache
                                 )
from api.serializers import SubscriptionSerializer
from blog_service.models import Subscription


def subscribe_logic(user, blog_id):
    cache_key = get_cache_key(user.id, blog_id)

    response = check_cache_and_return_response(
        cache_key,
        'You are already subscribed to this blog.',
        status.HTTP_400_BAD_REQUEST)
    if response:
        return response
    existing_subscription = Subscription.objects.filter(
        subscriber=user, blog_id=blog_id).exists()

    if existing_subscription:
        return Response(
            {'message': 'You are already subscribed to this blog.'},
            status=status.HTTP_400_BAD_REQUEST)
    new_subscription = perform_subscription(user, blog_id)
    set_cache(cache_key, 'subscribed')
    serialized_data = SubscriptionSerializer(new_subscription).data
    return Response(serialized_data, status=status.HTTP_201_CREATED)


def unsubscribe_logic(user, blog_id):
    cache_key = get_cache_key(user.id, blog_id)
    response = check_cache_and_return_response(
        cache_key,
        'You are not subscribed to this blog.',
        status.HTTP_400_BAD_REQUEST)
    if response:
        return response

    existing_subscription = Subscription.objects.filter(
        subscriber=user,
        blog_id=blog_id)
    if not existing_subscription.exists():
        return Response(
            {'message': 'You are not subscribed to this blog.'},
            status=status.HTTP_400_BAD_REQUEST)
    delete_subscription(existing_subscription)
    set_cache(cache_key, 'unsubscribed')
    return Response(
        {'message': 'Unsubscribed successfully.'},
        status=status.HTTP_200_OK)
