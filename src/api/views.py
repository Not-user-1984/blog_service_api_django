from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.subscriptions_logic import subscribe_logic, unsubscribe_logic
from api.serializers import (BlogSerializer, PostSerializer,
                             SubscriptionSerializer)
from blog_service.models import Blog, Post, PostRead, Subscription
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        post = self.get_object()
        user = request.user
        cache_key = f'post_read:{user.id}:{post.id}'
        post_read = cache.get(cache_key)
        if post_read is None:
            post_read, _ = PostRead.objects.get_or_create(user=user, post=post)
            if not post_read.is_read:
                post_read.is_read = True
                post_read.save()
            cache.set(cache_key, post_read, timeout=None)  # Хранить в кеше постоянно

        return Response({'message': 'Post marked as read.'},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def check_read_status(self, request, pk=None):
        post = self.get_object()
        user = request.user
        cache_key = f'post_read:{user.id}:{post.id}'
        is_read = cache.get(cache_key)
        if is_read is None:
            try:
                PostRead.objects.get(user=user, post=post)
                is_read = True
            except PostRead.DoesNotExist:
                is_read = False
            cache.set(cache_key, is_read, timeout=None)

        return Response({'is_read': is_read}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        post = self.get_object()
        user = request.user
        blog_id = post.blog.id
        if not blog_id:
            return Response(
                {'message': 'Missing blog_id in request.'},
                status=status.HTTP_400_BAD_REQUEST)
        return subscribe_logic(user, blog_id)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        subscript = self.get_object()
        user = request.user
        blog_id = subscript.blog.id

        if not blog_id:
            return Response(
                {'message': 'Missing blog_id in request.'},
                status=status.HTTP_400_BAD_REQUEST)
        return unsubscribe_logic(user, blog_id)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class PersonalFeedViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        subscribed_blogs = Subscription.objects.filter(
            subscriber=user).values_list('blog_id', flat=True)
        read_posts = PostRead.objects.filter(
            user=user, is_read=True).values_list('post_id',
                                                flat=True)
        queryset = Post.objects.filter(
            blog_id__in=subscribed_blogs,
            id__in=read_posts,
            is_read=False).order_by('-created_at')
        return queryset

    def perform_create(self, serializer):
        serializer.save()
    