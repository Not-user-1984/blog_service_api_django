import pytest
from django.db.utils import IntegrityError
from blog_service.models import Blog, Post, PostRead


@pytest.mark.django_db
def test_create_blog(blog, user):
    """
    Тест создания блога.
    """
    assert blog.name == "Блог testuser"
    assert blog.user == user


@pytest.mark.django_db
def test_update_blog_name(blog):
    """
    Тест обновления имени блога.
    """
    new_name = 'Обновленное имя блога'
    blog.name = new_name
    blog.save()
    updated_blog = Blog.objects.get(pk=blog.pk)
    assert updated_blog.name == new_name


@pytest.mark.django_db
def test_create_post(post, blog):
    """
    Тест создания поста.
    """
    assert post.title == 'Тестовый пост'
    assert post.text == 'Это контент тестового поста.'
    assert post.blog == blog


@pytest.mark.django_db
def test_update_post_text(post):
    """
    Тест обновления текста поста.
    """
    new_text = 'Обновленный текст поста'
    post.text = new_text
    post.save()
    updated_post = Post.objects.get(pk=post.pk)
    assert updated_post.text == new_text


@pytest.mark.django_db
def test_create_subscription(subscription, user, blog):
    """
    Тест создания подписки.
    """
    assert subscription.subscriber == user
    assert subscription.blog == blog


@pytest.mark.django_db
def test_update_subscription_blog(subscription, blog):
    """
    Тест обновления блога в подписке.
    """
    with pytest.raises(IntegrityError):
        new_blog = Blog.objects.create(
            name='Новый тестовый блог', user=blog.user)
        subscription.blog = new_blog
        subscription.save()


@pytest.mark.django_db
def test_create_post_read(post_read, user, post):
    """
    Тест создания отметки о прочтении поста.
    """
    assert post_read.user == user
    assert post_read.post == post
    assert not post_read.is_read


@pytest.mark.django_db
def test_update_post_read_status(post_read):
    """
    Тест обновления статуса прочтения поста.
    """
    post_read.is_read = True
    post_read.save()
    updated_post_read = PostRead.objects.get(pk=post_read.pk)
    assert updated_post_read.is_read
