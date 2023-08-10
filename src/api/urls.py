from django.urls import path

from api.views import (BlogListCreateView, CheckPostRead, MarkPostAsRead,
                       PersonalFeedView, PostListCreateView,
                       SubscriptionListCreateView)

urlpatterns = [
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'),
    path('mark_post_as_read/', MarkPostAsRead.as_view(), name='mark-post-as-read'),
    path('check_post_read/', CheckPostRead.as_view(), name='check-post-read'),
    path('personal_feed/', PersonalFeedView.as_view(), name='personal-feed'),
]
