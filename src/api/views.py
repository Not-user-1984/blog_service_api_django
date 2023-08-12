from django.core.cache import cache
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from api.serializers import (BlogSerializer, PostReadSerializer,
                             PostSerializer, SubscriptionSerializer)
from api.subscriptions_logic import subscribe_logic, unsubscribe_logic
from blog_service.models import Blog, Post, PostRead, Subscription


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Post.
    Позволяет маркировать посты как прочитанные
    и проверять их статус прочтения.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Маркирует пост как прочитанный.
        """
        post = self.get_object()
        user = request.user
        cache_key = f'post_read:{user.id}:{post.id}'
        post_read = cache.get(cache_key)
        if post_read is False:
            post_read = True
            cache.set(cache_key, post_read, timeout=None)
            return Response({'message': 'Post marked as read cache.'},
                            status=status.HTTP_200_OK)
        else:
            if post_read is None:
                post_read, _ = PostRead.objects.get_or_create(
                    user=user, post=post)
                if not post_read.is_read:
                    post_read.is_read = True
                    post_read.save()
                cache.set(cache_key, post_read, timeout=None)
        return Response({'message': 'Post marked as read.'},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def check_read_status(self, request, pk=None):
        """
        Проверяет статус прочтения поста.
        """
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

        serializer = PostReadSerializer({'is_read': is_read})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Blog. Позволяет подписываться и отписываться от блогов.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        blog_id = self.get_object().id
        if not blog_id:
            return Response(
                {'message': 'Missing blog_id in request.'},
                status=status.HTTP_400_BAD_REQUEST)
        return subscribe_logic(request.user, blog_id)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        blog_id = self.get_object().id
        if not blog_id:
            return Response(
                {'message': 'Missing blog_id in request.'},
                status=status.HTTP_400_BAD_REQUEST)
        return unsubscribe_logic(request.user, blog_id)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Subscription.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class PersonalFeedViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для получения персональной
    ленты пользователя с непрочитанными постами.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        subscribed_blogs = user.subscriptions.all().values_list(
            'blog',
            flat=True)
        unread_posts = Post.objects.filter(
            Q(blog__in=subscribed_blogs) &
            ~Q(postread__user=user, postread__is_read=True)
        ).order_by('-created_at')[:settings.MAX_UNREAD_POSTS_LIMIT]
        return unread_posts
