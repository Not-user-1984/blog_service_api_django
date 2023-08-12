import pytest
from blog_service.models import Blog, Post
from api.serializers import BlogSerializer
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_last_10_posts(user):
    """
    Тест получения последних 10 постов из блога.
    """
    blog = Blog.objects.get(user=user)
    for i in range(10):
        Post.objects.create(
            blog=blog, title=f"Пост {i}", text=f"Это пост {i}")

    serializer = BlogSerializer(blog)
    last_10_posts = serializer.get_last_10_posts(blog)

    assert len(last_10_posts) == 5
    assert last_10_posts[0]['title'] == "Пост 9"
    assert last_10_posts[4]['title'] == "Пост 5"


@pytest.mark.django_db
def test_cannot_create_duplicate_post(blog, user):
    """
    Тест на невозможность создания дубликата поста.
    """
    client = APIClient()
    client.force_authenticate(user=user)

    initial_post_count = Post.objects.count()

    data = {
        'blog': blog.id,
        'title': 'Тестовый пост',
        'text': 'Это тестовый пост',
    }

    response = client.post('/api/posts/', data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == initial_post_count + 1

    # Попробовать создать дубликат поста
    response = client.post('/api/posts/', data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Post.objects.count() == initial_post_count + 1
