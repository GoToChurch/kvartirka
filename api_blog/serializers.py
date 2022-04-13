from rest_framework import serializers

from .models import Blog, Post, Subscribe, SeenPosts, User


class BlogSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field="username",
                                          queryset=User.objects.all())
    class Meta:
        model = Blog
        fields = ("title", "url", "description", "created_at", "author")
        lookup_field = 'url'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field="username",
                                          queryset=User.objects.all())
    blog = serializers.SlugRelatedField(slug_field="title",
                                        queryset=Blog.objects.all())

    class Meta:
        model = Post
        fields = ("id", "h1", "title", "url", "description", "content", "created_at", "author", "blog")
        lookup_field = 'url'


class SubscribeSerializer(serializers.ModelSerializer):

    subscriber = serializers.SlugRelatedField(slug_field="username",
                                          queryset=User.objects.all())
    blog = serializers.SlugRelatedField(slug_field="title",
                                        queryset=Blog.objects.all())

    class Meta:
        model = Subscribe
        fields = '__all__'


class SeenPostSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field="username",
                                          queryset=User.objects.all())
    post = serializers.SlugRelatedField(slug_field="title",
                                        queryset=Post.objects.all())

    class Meta:
        model = SeenPosts
        fields = '__all__'
