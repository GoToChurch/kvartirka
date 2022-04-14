from django.contrib import admin

from .models import Blog, Comment, Post, SeenPosts, Subscribe,  User
from test_blog.admin import BlogAdmin, CommentInLine, PostAdmin, \
    SeenPostsAdmin, SubscribeAdmin
