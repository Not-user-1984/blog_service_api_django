import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.cache import cache
from blog_service.models import Blog, Post, Subscription, PostRead


@pytest.fixture(scope='function')
def reset_db():
    call_command('flush', '--noinput')


@pytest.fixture
def blog(user):
    return Blog.objects.get(user=user)


@pytest.fixture
def user():
    return User.objects.create(
        username='testuser', password='testpass'
        )


@pytest.fixture
def subscription(user, blog):
    return Subscription.objects.create(subscriber=user, blog=blog)


@pytest.fixture
def post_read(user, post):
    return PostRead.objects.create(user=user, post=post, is_read=False)

@pytest.fixture
def post(blog):
    return Post.objects.create(
        blog=blog,
        title='Test Post',
        text='This is a test post content.',
    )


@pytest.fixture
def post_read_cache(user, post):
    cache_key = f'post_read:{user.id}:{post.id}'
    cache.set(cache_key, False, timeout=None)
    return cache_key

