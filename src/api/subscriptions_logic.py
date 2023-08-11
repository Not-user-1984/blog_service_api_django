from rest_framework import status
from rest_framework.response import Response

from api.serializers import SubscriptionSerializer
from blog_service.models import Subscription


def subscribe_logic(user, blog_id):
    existing_subscription = Subscription.objects.filter(
        subscriber=user, blog_id=blog_id).exists()
    if existing_subscription:
        return Response(
            {'message': 'You are already subscribed to this blog.'},
            status=status.HTTP_400_BAD_REQUEST)
    new_subscription = Subscription.objects.create(
        subscriber=user,
        blog_id=blog_id)
    serialized_data = SubscriptionSerializer(new_subscription).data
    return Response(serialized_data, status=status.HTTP_201_CREATED)


def unsubscribe_logic(user, blog_id):
    existing_subscription = Subscription.objects.filter(
        subscriber=user,
        blog_id=blog_id)
    if not existing_subscription.exists():
        return Response(
            {'message': 'You are not subscribed to this blog.'},
            status=status.HTTP_400_BAD_REQUEST)
    existing_subscription.delete()
    return Response(
        {'message': 'Unsubscribed successfully.'},
        status=status.HTTP_200_OK)
