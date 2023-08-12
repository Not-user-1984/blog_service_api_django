import pytest
from blog_service.models import Post
from django.db.utils import IntegrityError
import pytest
from blog_service.models import Blog, Post, Subscription, PostRead


@pytest.mark.django_db
def test_create_blog(blog, user):
    assert blog.name == "testuser's Blog"
    assert blog.user == user


@pytest.mark.django_db
def test_update_blog_name(blog):
    new_name = 'Updated Blog Name'
    blog.name = new_name
    blog.save()
    updated_blog = Blog.objects.get(pk=blog.pk)
    assert updated_blog.name == new_name


@pytest.mark.django_db
def test_create_post(post, blog):
    assert post.title == 'Test Post'
    assert post.text == 'This is a test post content.'
    assert post.blog == blog


@pytest.mark.django_db
def test_update_post_text(post):
    new_text = 'Updated Post Text'
    post.text = new_text
    post.save()
    updated_post = Post.objects.get(pk=post.pk)
    assert updated_post.text == new_text


@pytest.mark.django_db
def test_create_subscription(subscription, user, blog):
    assert subscription.subscriber == user
    assert subscription.blog == blog


@pytest.mark.django_db
def test_update_subscription_blog(subscription, blog):
    with pytest.raises(IntegrityError):
        new_blog = Blog.objects.create(name='New Test Blog', user=blog.user)
        subscription.blog = new_blog
        subscription.save()


@pytest.mark.django_db
def test_create_post_read(post_read, user, post):
    assert post_read.user == user
    assert post_read.post == post
    assert not post_read.is_read


@pytest.mark.django_db
def test_update_post_read_status(post_read):
    post_read.is_read = True
    post_read.save()
    updated_post_read = PostRead.objects.get(pk=post_read.pk)
    assert updated_post_read.is_read
