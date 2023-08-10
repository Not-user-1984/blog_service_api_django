from django.urls import path

from api.views import (BlogListCreateView, PostListCreateView,
                    SubscriptionListCreateView)

urlpatterns = [
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'),
]
