from django.core.cache import cache
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from subscriptions_logic import subscribe_logic, unsubscribe_logic
from api.serializers import (BlogSerializer, PostSerializer,
                             SubscriptionSerializer)
from blog_service.models import Blog, Post, Subscription
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        post = self.get_object()
        if not post.is_read:
            post.is_read = True
            post.save()
            cache.set(f'post_{post.id}_read', True)

        return Response({'message': 'Post marked as read.'},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def check_read_status(self, request, pk=None):
        post = self.get_object()
        is_read = cache.get(f'post_{post.id}_read')
        if is_read is None:
            is_read = post.is_read

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
            return Response(
                {'message': 'Missing blog_id in request.'},
                status=status.HTTP_400_BAD_REQUEST)
        return subscribe_logic(user, blog_id, self.get_serializer)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        subscript = self.get_object()
        user = request.user
        blog_id = subscript.blog.id

        if not blog_id:
            return Response(
                {'message': 'Missing blog_id in request.'},
                status=status.HTTP_400_BAD_REQUEST)
        return unsubscribe_logic(user, blog_id, self.get_serializer)


class PersonalFeedViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination 

    def get_queryset(self):
        user = self.request.user
        subscribed_blogs = Subscription.objects.filter(
            subscriber=user).values_list('blog_id', flat=True)
        queryset = Post.objects.filter(
            blog_id__in=subscribed_blogs,
            is_read=False).order_by('-created_at')
        return queryset

    def perform_create(self, serializer):
        serializer.save()
