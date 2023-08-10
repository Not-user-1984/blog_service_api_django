import redis
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (BlogSerializer, PostSerializer,
                             SubscriptionSerializer)
from blog_service.models import Blog, Post, Subscription

redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        post = self.get_object()
        user = request.user
        post_id = post.id
        redis_ping = redis_client.ping()
        if not redis_ping:
            return Response(
                {'message': 'Redis connection error.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        read_posts_key = f'user:{user.id}:read_posts'
        redis_client.sadd(read_posts_key, post_id)

        return Response({'message': 'Post marked as read.'},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def check_read_status(self, request, pk=None):
        # Получение поста по pk
        post = self.get_object()

        user = request.user
        post_id = post.id

        # Проверка связи с Redis
        redis_ping = redis_client.ping()
        if not redis_ping:
            return Response({'message': 'Redis connection error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        read_posts_key = f'user:{user.id}:read_posts'
        is_read = redis_client.sismember(read_posts_key, post_id)

        return Response({'is_read': is_read}, status=status.HTTP_200_OK)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        user = request.user
        blog_id = request.data.get('blog_id')
        if not blog_id:
            return Response({'message': 'Missing blog_id in request.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_subscription = Subscription.objects.filter(subscriber=user, blog_id=blog_id).exists()
        if existing_subscription:
            return Response({'message': 'You are already subscribed to this blog.'}, status=status.HTTP_400_BAD_REQUEST)

        new_subscription = Subscription.objects.create(subscriber=user, blog_id=blog_id)
        serializer = self.get_serializer(new_subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        subscript= self.get_object()
        user = request.user
        blog_id = subscript.blog.id

        if not blog_id:
            return Response({'message': 'Missing blog_id in request.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_subscription = Subscription.objects.filter(subscriber=user, blog_id=blog_id)
        if not existing_subscription.exists():
            return Response({'message': 'You are not subscribed to this blog.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_subscription.delete()
        return Response({'message': 'Unsubscribed successfully.'}, status=status.HTTP_200_OK)


class PersonalFeedViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        subscribed_blogs = Subscription.objects.filter(
            subscriber=user).values_list('blog_id', flat=True)

        read_posts_key = f'user:{user.id}:read_posts'
        read_posts = redis_client.smembers(read_posts_key)

        queryset = Post.objects.filter(
            Q(blog_id__in=subscribed_blogs) & ~Q(id__in=read_posts)
        ).order_by('-created_at')[:10]
        return queryset