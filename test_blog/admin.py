from django.contrib import admin
from django.core.mail import send_mail
from .models import Post, Blog, Subscribe, SeenPosts, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')
    list_filter = ['created_at']

    def save_model(self, request, obj, form, change):
        '''Переопределяется метод сохранения модели'''

        user = request.user
        blog = Blog.objects.get(author=user)
        users = blog.subscribed_blog.values_list('subscriber', flat=True)
        send_mail(f'New post on {blog.title}',
                  f'{user} just posted new stuff on {blog.title}. Check it out!',
                  f'{user.email}', [f'{user.email}' for user in users])
        obj.save()
        SeenPosts.objects.get_or_create(user=user, post=obj)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')
    list_filter = ['created_at']

    def save_model(self, request, obj, form, change):
        '''Переопределяется метод сохранения модели'''
        user = request.user
        blog = Blog.objects.get(author=user)
        obj.save()
        Subscribe.objects.get_or_create(subscriber=user, blog=blog)

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'blog')

class SeenPostsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')

class CommentInLine(admin.TabularInline):
    model = Comment

admin.site.register(Post, PostAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(SeenPosts, SeenPostsAdmin)
