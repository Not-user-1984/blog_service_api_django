from django.contrib import admin
from blog_service.models import Blog, Post, Subscription, PostRead


class BlogAdmin(admin.ModelAdmin):
    list_display = ('user',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('blog', 'title', 'created_at')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'blog')


class PostReadAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_read')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(PostRead, PostReadAdmin)