import redis
from rest_framework import status
from rest_framework import generics
from django.db.models import Q
from api.serializers import (BlogSerializer, PostSerializer,
                             SubscriptionSerializer)
from blog_service.models import Blog, Post, Subscription
from rest_framework.views import APIView
from rest_framework.response import Response

redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True)


class MarkPostAsRead(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get('post_id')
        if post_id:
            read_posts_key = f'user:{user.id}:read_posts'
            redis_client.sadd(read_posts_key, post_id)

            return Response(
                {'message': 'Post marked as read.'},
                status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'message': 'Missing post_id in request.'},
                status=status.HTTP_400_BAD_REQUEST
                )


class CheckPostRead(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        post_id = request.query_params.get('post_id')

        if post_id:
            read_posts_key = f'user:{user.id}:read_posts'
            is_read = redis_client.sismember(read_posts_key, post_id)
            return Response(
                {'is_read': is_read}, status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'message': 'Missing post_id in request.'},
                status=status.HTTP_400_BAD_REQUEST
                )


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class SubscriptionListCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class PersonalFeedView(generics.ListAPIView):
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
