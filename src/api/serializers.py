from rest_framework import serializers
from blog_service.models import Blog, Post, Subscription, PostRead


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title","text")


class BlogSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Subscription
        fields = '__all__'


class PostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRead
        fields = ('is_read',)
