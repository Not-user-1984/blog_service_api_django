from rest_framework import serializers
from blog_service.models import Blog, Post, Subscription, PostRead


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.
    """
    class Meta:
        model = Post
        fields = '__all__'

    def validate(self, data):
        """
        Проверяет, не существует ли уже пост с таким же заголовком и текстом.
        """
        title = data.get('title')
        text = data.get('text')

        if Post.objects.filter(title=title, text=text).exists():
            raise serializers.ValidationError(
                "Post with the same title and text already exists.")

        return data


class PostBlogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post с полями 'title' и 'text'.
    """
    class Meta:
        model = Post
        fields = ("title", "text",)


class BlogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Blog,
    включая информацию о пользователе и последних 10 постах.
    """
    user = serializers.SerializerMethodField()
    last_10_posts = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ("id", "name", "user", "last_10_posts",)

    def get_user(self, obj):
        return obj.user.username

    def get_last_10_posts(self, obj):
        posts = Post.objects.filter(blog=obj).order_by('-created_at')[:5]
        serialized_posts = PostBlogSerializer(posts, many=True).data
        return serialized_posts


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Subscription.
    """
    class Meta:
        model = Subscription
        fields = '__all__'


class PostReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели PostRead.
    """
    class Meta:
        model = PostRead
        fields = ('is_read',)
