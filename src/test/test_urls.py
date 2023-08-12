import pytest
from django.urls import reverse
from rest_framework import status
from blog_service.models import  Subscription


@pytest.mark.django_db
def test_mark_as_read(client, user, post):
    client.force_login(user)
    url = reverse('post-mark-as-read', args=[post.pk])
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_check_read_status(client, user, post, post_read_cache):
    client.force_login(user)
    url = reverse('post-check-read-status', args=[post.pk])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_subscribe_to_blog(client, user, blog):
    client.force_login(user)
    url = reverse('blog-subscribe', kwargs={'pk': blog.pk})
    response = client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert Subscription.objects.filter(subscriber=user, blog=blog).exists()


@pytest.mark.django_db
def test_unsubscribe_from_blog(client, user, subscription):
    client.force_login(user)
    url = reverse('blog-unsubscribe', kwargs={'pk': subscription.blog.pk})
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert not Subscription.objects.filter(subscriber=user, blog=subscription.blog).exists()


@pytest.mark.django_db
def test_view_blog_posts(client, blog, post):
    url = reverse('blog-posts', kwargs={'pk': blog.pk})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_view_personal_feed(client, user):
    client.force_login(user)
    url = reverse('personal-feed-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_view_all_blogs(client):
    url = reverse('blog-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK






