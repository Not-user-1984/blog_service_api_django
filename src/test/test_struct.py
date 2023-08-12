import pytest
from blog_service.models import Blog, Post
from api.serializers import BlogSerializer
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_last_10_posts(user):
    blog = Blog.objects.get(user=user)
    for i in range(10):
        Post.objects.create(
            blog=blog, title=f"Post {i}", text=f"This is post {i}")

    serializer = BlogSerializer(blog)
    last_10_posts = serializer.get_last_10_posts(blog)

    assert len(last_10_posts) == 5
    assert last_10_posts[0]['title'] == "Post 9"
    assert last_10_posts[4]['title'] == "Post 5"


@pytest.mark.django_db
def test_cannot_create_duplicate_post(blog, user):
    client = APIClient()
    client.force_authenticate(user=user)

    initial_post_count = Post.objects.count()

    data = {
        'blog': blog.id,
        'title': 'Test Post',
        'text': 'This is a test post',
    }

    response = client.post('/api/posts/', data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == initial_post_count + 1

    # Try creating a duplicate post
    response = client.post('/api/posts/', data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Post.objects.count() == initial_post_count + 1
