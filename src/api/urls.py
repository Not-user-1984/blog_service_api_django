from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BlogViewSet, PersonalFeedViewSet, PostViewSet,
                    SubscriptionViewSet)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'subscriptions',
                SubscriptionViewSet, basename='subscription')
router.register(r'personal_feed',
                PersonalFeedViewSet, basename='personal-feed')


urlpatterns = [
    path('', include(router.urls)),
]
